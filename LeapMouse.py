import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, Finger
import mouse

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
        previous = controller.frame(10)
        
        '''print "Frame ID: " + str(frame.id) \
        	+ " TimeStamp " + str(frame.timestamp) \
        	+ " # of Hands " + str(len(frame.hands)) \
        	+ " # of Fingers " + str(len(frame.fingers)) \
        	+ " # of Tools " + str(len(frame.tools)) \
        	+ " Gesure: " + str(len(frame.gestures()))'''
        
        frame_pointer = None
        prev_frame_pointer = None

        for i in range(len(frame.pointables)):
            if (Finger(frame.pointables[i]).type == 1) and (frame.pointables[i].hand.is_right):
                frame_pointer = frame.pointables[i]
            if (Finger(previous.pointables[i]).type == 1) and (previous.pointables[i].hand.is_right):
                prev_frame_pointer = previous.pointables[i]

        if (frame_pointer is not None and prev_frame_pointer is not None) and (Finger(frame_pointer).type == 1) and (Finger(prev_frame_pointer).type == 1):
            frame_pointer = frame_pointer.stabilized_tip_position
            prev_frame_pointer = prev_frame_pointer.stabilized_tip_position
            x = frame_pointer[0] - prev_frame_pointer[0]
            y = prev_frame_pointer[1] -  frame_pointer[1]

            mouse.move(x, y, absolute=False, duration=0)
        #print str(prev_frame_pointer[0])
        #print str(frame_pointer[0])
        #print



        '''for i in range(len(frame_pointables)):
            print len(frame_pointables)
            pointer = frame_pointables[i]
            print "point: " + str(pointer.id) + " " +  str(pointer.tip_position)
            print "stablized position "+str(pointer.stabilized_tip_position)
            print'''

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, contoller):
        print "Done"

    def move_cursor():
        return 

def main():
    # Create a sample listener and controller
    listener = LeapListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
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


