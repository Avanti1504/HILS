//Standard libraries
#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<string.h>


 #include "image_1.h"
 #include "image_2.h" 
 #include "image_3.h" 
 #include "image_4.h" 
 #include "image_5.h" 
 #include "image_6.h" 
 #include "image_7.h" 
 #include "image_8.h" 
 #include "image_9.h" 
 #include "image_10.h"
 #include "image_11.h"
 #include "image_12.h"
 #include "image_13.h"
 #include "image_14.h"
 #include "image_15.h"
 #include "image_16.h"
 #include "image_17.h"
 #include "image_18.h"
 #include "image_19.h"
 #include "image_20.h"
 #include "image_21.h"
 #include "image_22.h"
 #include "image_23.h"
 #include "image_24.h"
 #include "image_25.h"
 #include "image_26.h"
 #include "image_27.h"
 #include "image_28.h"
 #include "image_29.h"
 #include "image_30.h"
 #include "image_31.h"
 #include "image_32.h"
 #include "image_33.h"
 #include "image_34.h"
 #include "image_35.h"
 #include "image_36.h"
 #include "image_37.h"
 #include "image_38.h"
 #include "image_39.h"
 #include "image_40.h"
 #include "image_41.h"
 #include "image_42.h"
 #include "image_43.h"
 #include "image_44.h"
 #include "image_45.h"
 #include "image_46.h"
 #include "image_47.h"
 #include "image_48.h"
 #include "image_49.h"
 #include "image_50.h"
 #include "image_51.h"
 #include "image_52.h"
 #include "image_53.h"
 #include "image_54.h"
 #include "image_55.h"
 #include "image_56.h"
 #include "image_57.h"
 #include "image_58.h"
 #include "image_59.h"
 #include "image_60.h"
 #include "image_61.h"
 #include "image_62.h"
 #include "image_63.h"
 #include "image_64.h"
 #include "image_65.h"
 #include "image_66.h"
 #include "image_67.h"
 #include "image_68.h"
 #include "image_69.h"
 #include "image_70.h"
 #include "image_71.h"
 #include "image_72.h"
 #include "image_73.h"
 #include "image_74.h"
 #include "image_75.h"
 #include "image_76.h"
 #include "image_77.h"
 #include "image_78.h"
 #include "image_79.h"
 #include "image_80.h"
 #include "image_81.h"
 #include "image_82.h"
 #include "image_83.h"
 #include "image_84.h"
 #include "image_85.h"
 #include "image_86.h"
 #include "image_87.h"
 #include "image_88.h"
 #include "image_89.h"
 #include "image_90.h"
 #include "image_91.h"
 #include "image_92.h"
 #include "image_93.h"
 #include "image_94.h"
 #include "image_95.h"
 #include "image_96.h"
 #include "image_97.h"
 #include "image_98.h"
 #include "image_99.h"
 #include "image_100.h"

float threshold_vals[100];
int threshold(short array[BREADTH + 2][LENGTH + 2],int m)
{
    double p_mean = 0;
    double p_sd = 0;
    double TH = 0;

    for(int i = 0; i < BREADTH; i++)
    {
        for(int j = 0; j < LENGTH; j++)
        {
            p_mean += array[i][j];
            p_sd += array[i][j]*array[i][j];
        }
    }
    //printf("Mean value is %f\n", p_mean);

    p_mean = p_mean/(LENGTH*BREADTH);
    p_sd = sqrt(p_sd/(LENGTH*BREADTH) - p_mean*p_mean);

    TH = p_mean + 5*p_sd;

    //printf("Mean value is %f\n", p_mean);
    //printf("Standard Deviation is %f\n", p_sd);
    printf("%f\n", TH);
    return 0;
}
int main()
{
threshold(arr_out_img_1,1); 
threshold(arr_out_img_2,2); 
threshold(arr_out_img_3,3); 
threshold(arr_out_img_4,4); 
threshold(arr_out_img_5,5); 
threshold(arr_out_img_6,6); 
threshold(arr_out_img_7,7); 
threshold(arr_out_img_8,8); 
threshold(arr_out_img_9,9); 
threshold(arr_out_img_10,10); 
threshold(arr_out_img_11,11); 
threshold(arr_out_img_12,12); 
threshold(arr_out_img_13,13); 
threshold(arr_out_img_14,14); 
threshold(arr_out_img_15,15); 
threshold(arr_out_img_16,16); 
threshold(arr_out_img_17,17); 
threshold(arr_out_img_18,18); 
threshold(arr_out_img_19,19); 
threshold(arr_out_img_20,20); 
threshold(arr_out_img_21,21); 
threshold(arr_out_img_22,22); 
threshold(arr_out_img_23,23); 
threshold(arr_out_img_24,24); 
threshold(arr_out_img_25,25); 
threshold(arr_out_img_26,26); 
threshold(arr_out_img_27,27); 
threshold(arr_out_img_28,28); 
threshold(arr_out_img_29,29); 
threshold(arr_out_img_30,30); 
threshold(arr_out_img_31,31); 
threshold(arr_out_img_32,32); 
threshold(arr_out_img_33,33); 
threshold(arr_out_img_34,34); 
threshold(arr_out_img_35,35); 
threshold(arr_out_img_36,36); 
threshold(arr_out_img_37,37); 
threshold(arr_out_img_38,38); 
threshold(arr_out_img_39,39); 
threshold(arr_out_img_40,40); 
threshold(arr_out_img_41,41); 
threshold(arr_out_img_42,42); 
threshold(arr_out_img_43,43); 
threshold(arr_out_img_44,44); 
threshold(arr_out_img_45,45); 
threshold(arr_out_img_46,46); 
threshold(arr_out_img_47,47); 
threshold(arr_out_img_48,48); 
threshold(arr_out_img_49,49); 
threshold(arr_out_img_50,50); 
threshold(arr_out_img_51,51); 
threshold(arr_out_img_52,52); 
threshold(arr_out_img_53,53); 
threshold(arr_out_img_54,54); 
threshold(arr_out_img_55,55); 
threshold(arr_out_img_56,56); 
threshold(arr_out_img_57,57); 
threshold(arr_out_img_58,58); 
threshold(arr_out_img_59,59); 
threshold(arr_out_img_60,60); 
threshold(arr_out_img_61,61); 
threshold(arr_out_img_62,62); 
threshold(arr_out_img_63,63); 
threshold(arr_out_img_64,64); 
threshold(arr_out_img_65,65); 
threshold(arr_out_img_66,66); 
threshold(arr_out_img_67,67); 
threshold(arr_out_img_68,68); 
threshold(arr_out_img_69,69); 
threshold(arr_out_img_70,70); 
threshold(arr_out_img_71,71); 
threshold(arr_out_img_72,72); 
threshold(arr_out_img_73,73); 
threshold(arr_out_img_74,74); 
threshold(arr_out_img_75,75); 
threshold(arr_out_img_76,76); 
threshold(arr_out_img_77,77); 
threshold(arr_out_img_78,78); 
threshold(arr_out_img_79,79); 
threshold(arr_out_img_80,80); 
threshold(arr_out_img_81,81); 
threshold(arr_out_img_82,82); 
threshold(arr_out_img_83,83); 
threshold(arr_out_img_84,84); 
threshold(arr_out_img_85,85); 
threshold(arr_out_img_86,86); 
threshold(arr_out_img_87,87); 
threshold(arr_out_img_88,88); 
threshold(arr_out_img_89,89); 
threshold(arr_out_img_90,90); 
threshold(arr_out_img_91,91); 
threshold(arr_out_img_92,92); 
threshold(arr_out_img_93,93); 
threshold(arr_out_img_94,94); 
threshold(arr_out_img_95,95); 
threshold(arr_out_img_96,96); 
threshold(arr_out_img_97,97); 
threshold(arr_out_img_98,98); 
threshold(arr_out_img_99,99); 
threshold(arr_out_img_100,100); 
return 0;
}