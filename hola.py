import os
os.environ.update({"QT_QPA_PLATFORM_PLUGIN_PATH": "/usr/lib/aarch64-linux-gnu/qt5/plugins/xcbglintegrations/libqxcb-glx-integration.so"})
"""import os, sys
ci_build_and_not_headless = False
try:
    from cv2.version import ci_build, headless
    ci_and_not_headless = ci_build and not headless
except:
    pass
if sys.platform.startswith("linux") and ci_and_not_headless:
    os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")
if sys.platform.startswith("linux") and ci_and_not_headless:
    os.environ.pop("QT_QPA_FONTDIR")"""