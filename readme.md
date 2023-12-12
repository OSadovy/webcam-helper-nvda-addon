# Webcam helper NVDA Addon
This addon for [NVDA], a free and open source screen reader for Microsoft Windows helps you to get a better shot at video calls by giving instructions about how to position yourself in front of camera. It uses facial recognition and image processing to detect if you are off to either side or vertically, as well as if the ilumination is enough.

# Instalation
This addon contains binary dependencies which require Visual C++ Redistributable for 32-bit platform, [direct download from Icrosoft](https://aka.ms/vs/17/release/vc_redist.x86.exe)

# Usage
After installing the addon, press NVDA+shift+w and follow the instructions. After you hear the message "The face is well positioned" - you can press the escape key to stop the function and release your camera.

# Development conventions
Since this is an addon for NVDA, the code runs inside the screen reader process, so it has to work under a specific runtime (Python 3.7 32bit) and bring its dependencies with itself. Also established code style in NVDA is different from that of pep8 for historical reasons, but it is followed here for consistency.

[NVDA]: https://github.com/nvaccess/nvda
