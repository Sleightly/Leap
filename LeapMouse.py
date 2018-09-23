import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, Finger
import mouse
import math

clicked = False
mode = 0

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
        self.change_mode(controller)
        global mode
        if mode == 0:
            self.pointer_mode(controller, 0)
        elif mode == 1:
            self.pointer_mode(controller, 0)
        elif mode == 2:
            self.gesture_mode(controller)





        #print str(prev_frame_pointer[0])
        #print str(frame_pointer[0])
        #print

        '''print "Frame ID: " + str(frame.id) \
            + " TimeStamp " + str(frame.timestamp) \
            + " # of Hands " + str(len(frame.hands)) \
            + " # of Fingers " + str(len(frame.fingers)) \
            + " # of Tools " + str(len(frame.tools)) \
            + " Gesure: " + str(len(frame.gestures()))'''

        '''for i in range(len(frame_pointables)):
            print len(frame_pointables)
            pointer = frame_pointables[i]
            print "point: " + str(pointer.id) + " " +  str(pointer.tip_position)
            print "stablized position "+str(pointer.stabilized_tip_position)
            print'''

    def change_mode(self, controller):
        frame = controller.frame()
        left_thumb = None
        left_index = None
        left_mid = None
        left_ring = None
        left_pinky = None

        for i in range(len(frame.pointables)):
            if frame.pointables[i].hand.is_left:
                if Finger(frame.pointables[i]).type == 0:
                    left_thumb = Finger(frame.pointables[i])
                if Finger(frame.pointables[i]).type == 1:
                    left_index = Finger(frame.pointables[i])
                if Finger(frame.pointables[i]).type == 2:
                    left_mid = Finger(frame.pointables[i])
                if Finger(frame.pointables[i]).type == 3:
                    left_ring = Finger(frame.pointables[i])
                if Finger(frame.pointables[i]).type == 4:
                    left_pinky = Finger(frame.pointables[i])

        if left_index is not None and left_mid is not None:
            global mode
            lt = left_thumb.is_extended
            li = left_index.is_extended
            lm = left_mid.is_extended
            lr = left_ring.is_extended
            lp = left_pinky.is_extended

            if li and not lm and not lt and not lp and mode is not 0:
                mode = 0
                print("pointer mode")
                return
            elif li and lm and not lt and not lp and mode is not 1:
                mode = 1
                print("slow pointer mode")
                return
            elif li and lm and lt and not lp and mode is not 2:
                mode = 2
                print("gesture mode")
                return
            elif li and lm and lr and lp and mode is not 3:
                mode = 3
                print("mode 4")
                return

    def pointer_mode(self, controller, speed):
        frame = controller.frame()
        previous = controller.frame(10)
        past = controller.frame(20)
        
        
        right_thumb = None
        right_index = None
        prev_right_index = None
       


        for i in range(len(frame.pointables)):
            if frame.pointables[i].hand.is_right:
                if Finger(frame.pointables[i]).type == 0:
                    right_thumb = Finger(frame.pointables[i])

                if Finger(frame.pointables[i]).type == 1:
                    right_index = frame.pointables[i]
                if Finger(previous.pointables[i]).type == 1:
                    prev_right_index = previous.pointables[i]

        #movement of mouse pointer
        if right_index is not None and prev_right_index is not None:
            right_index = right_index.stabilized_tip_position
            prev_right_index = prev_right_index.stabilized_tip_position
        
            x =(right_index[0] - prev_right_index[0])/1.2
            y = (prev_right_index[1] -  right_index[1])/1.2
            if speed > 0:
                x = (right_index[0] - prev_right_index[0])/speed
                y = (prev_right_index[1] -  right_index[1])/speed
            mouse.move(x, y, absolute=False, duration=0)
       
        #right click
        if right_thumb is not None:
            global clicked
            if right_thumb.is_extended and not clicked:
                clicked = True
                mouse.click()
                print("Thumb extended")

            if not right_thumb.is_extended and clicked:
                clicked = False
                print("Thumb not extended")
                print()

    def gesture_mode(self, controller):
        frame = controller.frame()
      
        frame_swipe = None

        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)
                frame_swipe = swipe.direction

        if frame_swipe is not None: 
            y = (frame_swipe[1]) * 2
            mouse.wheel(y)


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


