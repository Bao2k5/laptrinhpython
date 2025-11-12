@echo off
title Test Microphone for Breath Control
color 0B
echo ====================================
echo   TEST MICROPHONE
echo ====================================
echo.
echo Testing your microphone...
echo Speak or blow into the mic!
echo.
echo Press Ctrl+C to stop
echo.
python breath_controller.py
pause

