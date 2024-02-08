@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Set your image file path here
SET imageFilePath=.\image_1.jpg

:: Set the destination path on AVD
SET destinationPath=/sdcard/Pictures/image_1.jpg

:: Push the image to the AVD
adb push !imageFilePath! !destinationPath!

:: Trigger the media scanner
adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://!destinationPath!

:: Wait for 30 seconds
TIMEOUT /T 30

:: Delete the photo from the AVD
adb shell rm !destinationPath!

ENDLOCAL
