# Copyright (C) 2023 Oleksii Sadovyi

import os
import threading
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "3rdparty"))
# ruff: noqa: E402
# import cv2
# on some machines cv2 binary extension seems to load only after certain time (antivirus?)
import numpy as np
from yuface import detect

import addonHandler
import globalPluginHandler
import scriptHandler
import ui

addonHandler.initTranslation()


def detect_face(frame):
	import cv2  # ruff: noqa: E402

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	confs, bboxes, landmarks = detect(frame, conf=0.8)
	for bbox in bboxes:
		x, y, w, h = bbox
		return (int(x), int(y), int(w), int(h)), gray[y : y + h, x : x + w]
	return None, None


def calculate_brightness(face_gray):
	if face_gray is None or face_gray.size == 0:
		return 0
	return np.mean(face_gray)


def generate_lighting_advice(brightness):
	brightness_percent = round(brightness / 255 * 100, 0)
	if brightness_percent < 20:  # Threshold for low brightness
		return _("The lighting is too dim, consider increasing it")
	elif brightness_percent > 80:  # Threshold for high brightness
		return _("The lighting is too bright, consider reducing it")
	return ""


def generate_instructions(face_position, face_gray, frame_shape):
	if not face_position:
		return _("No face detected")

	x, y, w, h = face_position
	frame_center_x, frame_center_y = (
		frame_shape[1] // 2,
		frame_shape[0] // 3,
	)  # Targeting upper center
	face_center_x, face_center_y = x + w // 2, y + h // 2

	horizontal_move = ""
	vertical_move = ""
	distance_move = ""
	cropping = ""

	# Horizontal position
	if abs(face_center_x - frame_center_x) > frame_shape[1] * 0.1:  # More than 10% off center horizontally
		horizontal_move = _("Move right") if face_center_x > frame_center_x else _("Move left")

	# Vertical position
	if abs(face_center_y - frame_center_y) > frame_shape[0] * 0.1:  # More than 10% off center vertically
		vertical_move = _("Move up") if y + h / 2 > frame_center_y else _("Move down")

	# detect possible cropping - the face is too close to the frame edge
	cropping_factor = 0.03
	if x < cropping_factor * frame_shape[1]:
		cropping = _("possible cropping on the left")
	if x + w > (1 - cropping_factor) * frame_shape[1]:
		cropping = _("possible cropping on the right")
	if y < cropping_factor * frame_shape[0]:
		cropping = _("possible cropping on the top")
	if y + h > (1 - cropping_factor) * frame_shape[0]:
		cropping = _("possible cropping on the bottom")

	# Distance from camera
	face_area = w * h
	ideal_area = frame_shape[0] * frame_shape[1] * 0.1  # Assuming ideal face area is 10% of frame
	face_area_percent = round(face_area / (frame_shape[0] * frame_shape[1]) * 100)
	if face_area_percent < 4 or face_area_percent > 12:  # More than 20% difference in area
		distance_move = _("Move closer") if face_area < ideal_area else _("Move back")

	brightness = calculate_brightness(face_gray)
	lighting_advice = generate_lighting_advice(brightness)

	instructions = [
		horizontal_move,
		vertical_move,
		cropping,
		distance_move,
		lighting_advice,
	]
	return ", ".join(filter(None, instructions)) or "Face well positioned"


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super().__init__()
		self._stop_analysis = threading.Event()
		self._thread = None

	@scriptHandler.script(
		gesture="kb:NVDA+shift+w", description=_("Starts continuous webcam analysis, press escape to cancel")
	)
	def script_webcam_analysis(self, gesture):
		if self._thread:
			self._stop_analysis.set()
			self._thread.join()
			self._thread = None
			return
		ui.message(_("Starting webcam analysis, press escape key to stop"))
		self._stop_analysis.clear()
		self._thread = threading.Thread(target=self.doWebcamAnalysis)
		self._thread.start()
		self.bindGesture("kb:escape", "webcam_analysis_stop")

	def doWebcamAnalysis(self):
		try:
			self._doWebcamAnalysis()
		finally:
			try:
				self.removeGestureBinding("kb:escape")
			except LookupError:
				pass

	def _doWebcamAnalysis(self):
		import cv2  # ruff: noqa: E402

		cap = cv2.VideoCapture(0)
		if not cap.isOpened():
			ui.message(_("Failed to open webcam"))
			return

		last_instructions = ""

		while not self._stop_analysis.is_set():
			ret, frame = cap.read()
			if not ret:
				break

			face_position, face_gray = detect_face(frame)
			instructions = generate_instructions(face_position, face_gray, frame.shape)

			if instructions != last_instructions:
				ui.message(instructions)
				last_instructions = instructions
			self._stop_analysis.wait(0.5)

		cap.release()

	def script_webcam_analysis_stop(self, gesture):
		self.finish()
		ui.message(_("Webcam analysis stopped"))

	def finish(self):
		if self._thread:
			self._stop_analysis.set()
			self._thread.join()
			self._thread = None
