# PRISM Security Suite - Protocol Response Interface for Systems Management
# Copyright (C) HYPE Industries Military Defense Division - All Rights Reserved (HYPE-MMD)
# Dissemination of this information or reproduction of this material is strictly forbidden unless prior written permission is obtained from HYPE Industries.
# Written by Evan Sellers <sellersew@gmail.com>, April 2020 (CORONA-VACATION)

import cv2;
import argparse;
import sys;
import os;
import time;
from os import system


parser = argparse.ArgumentParser( description="Hyper Timelapse for Prism" );
parser.add_argument( "--output","-o",required=True, help="set the output directory" );
parser.add_argument( "--delay", "-d",required=True,type=float, help="seconds between picture" );
parser.add_argument( "--camera", "-c",default="0", help="camera IP address or web camera number (openCV)" );
parser.add_argument( "--motion", action="store_true", help="[Flag] Only Capture image if motion between delay frames" );
parser.add_argument( "--sensitivity", "-s",default="0.03", type=float, help="How sentive the motion detector is." );
args = parser.parse_args()
system( "title "+"Hype Timelapse Program" );

print(args.sensitivity)

# check to make sure directory exists
if not os.path.isdir( os.path.join( os.getcwd(), args.output ) ):
    print( "[ ERROR ] The directory you have selected doesn't exist" );
    sys.exit();

# Check for delay time
if args.delay <= 0:
    print( "[ ERROR ] Delay must be a integer larger than 0." );
    sys.exit();

# try to convert
try:
    args.camera = int( args.camera );
    print( "Connecting to web camera " + str( args.camera ) );
except:
    print( "Connecting to IP camera " + args.camera );


# Attempt to connect to camera
try:
    cam = cv2.VideoCapture( args.camera );
    if not cam.isOpened():
        raise;
except:
    print( "[ ERROR ] Error connecting to camera." );
    sys.exit();


# Camera Loop
print( "Press [Esc] to exit program" );
wait = time.time();
screen_shot = 0;
_, last_frame = cam.read();
size = int( cam.get( 3 ) * cam.get( 4 ) );
path = os.path.join( os.getcwd(), args.output );
while True:
    _, frame = cam.read()
    cv2.imshow( "Hyper Timelapse for Prism", cv2.flip( frame, 1 ) );
    if wait < time.time():
        capture = True;
        _frame  = frame;

        if args.motion == True:
            try:
                _frame  = cv2.cvtColor( _frame, cv2.COLOR_BGR2GRAY );
                last_frame = cv2.cvtColor( last_frame, cv2.COLOR_BGR2GRAY );
                _frame  = cv2.GaussianBlur( _frame, ( 21, 21 ), 0 );
                last_frame  = cv2.GaussianBlur( last_frame, ( 21, 21 ), 0 );
                diff_frame = cv2.absdiff( _frame, last_frame );
                diff_frame = cv2.threshold( diff_frame, 30, 255, cv2.THRESH_BINARY )[1];
                diff_frame = cv2.dilate( diff_frame, None, iterations = 2 );
                if int( cv2.countNonZero( diff_frame ) ) / size < args.sensitivity:
                    capture = False;
            except:
                capture = False;

        if capture == True:
            try:
                print( os.path.join( path, "img_" + str( int( time.time() ) ) + "_n" + str( screen_shot ) + ".jpg" ) )
                # cv2.imwrite( os.path.join( path, "img_" + str( int( time.time() ) ) + "_n" + str( screen_shot ) + ".jpg" ), frame );
            except:
                print( "[ ERRROR ] Writing File" );
        if args.delay > 3: # only print if time delay great enough
            print( "Screenshot: " + str( screen_shot ) );
        screen_shot = screen_shot + 1;
        wait = time.time() + args.delay;
        last_frame = frame;
    if cv2.waitKey( 1 ) == 27:
        break  # esc to quit
cv2.destroyAllWindows()
