# Rubik3D
A program that simulates the Rubik cube of an order less than 9

This program simulates the normal Rubik in in 3D cases. It has six faces named by Front(F), Down(D), Back(B), Up(U), Left(L) and Right(R).

Basics operations:

In order to control the Rubik, you need to type each motion or motions in the input bar named 'Motion'. Motions in this input bar must be splitted by delimiters such as ',' or ';'.

The basic motion elements are F, D, B, U, L and R, corresponding to each face. 

There are also two elements 'A' and 'T' corresponds to directions: A -> clockwise; T -> counter-clockwise; (This direction is the face that toward you. 
For instance, when you want to turn the back of the Rubik clockwise, you need to at least 'imagine' to rotate the backside toward you, then rotate clockwise)

Standard input contains four parts: Direction + end line + side + start line, for example, 
1. A3f1 means turn front side 1-3 lines clockwise; 
2. T2d2 means turn the down side only second line counter-clockwise;

Moreover, the direction 'A' can somehow be ommitted if there is no ambiguous. For example,
1. A3f1 == 3f1

When the order of the rubik is 3, then the rubik enters the simple mode, which
1. f = 1f1, d = 1d1, b = 1b1, etc. This means that the face elements are direct controls each face.

There are also several operation that helps to use:
1. Left and right arrow keys will rotate the rubik horizontally, which means the front side will also change correspondingly.
2. Up and down arrow keys will rotate the rubik vertically similar to the above case.
3. Keys '[' and ']' will also rotate the rubik while the front face will not change but rotate correspondingly, such that L->U->R->D->L or R->U->L->D->R.
4. The 'Reset View' button will reset the view of the rubik to make each face to its supposed position.

Shuffle:

If you want to shuffle the rubik and reset it by yourself, you can use the shuffle button at the bottom of the window. It will give a result that obtained from certain number of random steps.

Save and Load:

1. If you want to save the current status of the rubik, use the 'Save' button.
2. When you want to resume a play, use the 'Load' button to upload the saved status. 


A video example can be found in WeChat Public Platform:  https://mp.weixin.qq.com/s/Fss7bNh1MIXv0iqKAUoCfw
