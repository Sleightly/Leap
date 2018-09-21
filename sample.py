import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapListener(Leap.Listener):
    finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']
    bone_name = ['metacarpal', 'proximal', 'intermediate', 'distal']
    state_names = ['Invalid', 'Start', 'Update', 'End'] 

    def on_connect(self, controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);


    def on_frame(self, controller):
        frame = controller.frame()
        
        print "Frame ID: " + str(frame.id) \
        	+ " TimeStamp " + str(frame.timestamp) \
        	+ " # of Hands " + str(len(frame.hands)) \
        	+ " # of Fingers " + str(len(frame.fingers)) \
        	+ " # of Tools " + str(len(frame.tools)) \
        	+ " Gesure: " + str(len(frame.gestures()))
        

        #for hand in frame.hands:
        #	hand

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, contoller):
        print "Done"


def main():
    # Create a sample listener and controller
    print "here"
    listener = LeapListener()
    print "there"
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    print"here?"
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()


