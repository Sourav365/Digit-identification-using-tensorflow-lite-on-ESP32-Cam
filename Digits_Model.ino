#include <EloquentTinyML.h>

#include "digits_model.h"

#define NUMBER_OF_INPUTS 64
#define NUMBER_OF_OUTPUTS 10
#define TENSOR_ARENA_SIZE 8*1024

Eloquent::TinyML::TfLite<NUMBER_OF_INPUTS, NUMBER_OF_OUTPUTS, TENSOR_ARENA_SIZE> ml;

int i = 0;
String data1;

void setup() {
    Serial.begin(115200);
    ml.begin(digits_model);
}

void loop() {
   
    // Give data from Serial monitor
    if(Serial.available()>0){
      //Serial.print("Entered Data:");
      fflush;
      data1 = Serial.readString();
      
      int j =0;
      int len = 0,lasti = 0 ;
      float x_test [64]; 
  
      len = data1.length();
      
      while(i<len){
        if ( data1[i] == ','){
          data1.substring(lasti,i);
          String temp = data1.substring(lasti+1,i);
          temp.trim();
          //Serial.print(temp);
          //Serial.print("\t");
          x_test [j++] = float(temp.toFloat());
          lasti = i;
        }
        i++;
      }
      
      
  /*    float x_test[64] = { 0., 0. , 0.625 , 0.875 , 0.5   , 0.0625, 0. , 0. ,
                      0. , 0.125 , 1. , 0.875 , 0.375 , 0.0625, 0. , 0. ,
                      0. , 0. , 0.9375, 0.9375, 0.5   , 0.9375, 0. , 0. ,
                      0. , 0. , 0.3125, 1. , 1. , 0.625 , 0. , 0. ,
                      0. , 0. , 0.75  , 0.9375, 0.9375, 0.75  , 0. , 0. ,
                      0. , 0.25  , 1. , 0.375 , 0.25  , 1. , 0.375 , 0. ,
                      0. , 0.5   , 1. , 0.625 , 0.5   , 1. , 0.5   , 0. ,
                      0. , 0.0625, 0.5   , 0.75  , 0.875 , 0.75  , 0.0625, 0. };
      */

       
      float y_pred[10] = {0};
      
      ml.predict(x_test,y_pred);
      
      //Serial.println();
      Serial.print("Predicted values of different classes are: ");
  
      for ( i = 0; i < 10; i++) {
          Serial.print(y_pred[i]);
          Serial.print(i == 9 ? '\n' : ',');
      }
  
      // print the "most probable" class
      // you can either use probaToClass() if you also want to use all the probabilities
      Serial.print("Predicted class is: ");
      Serial.println(ml.probaToClass(y_pred));
      
      /*/ or you can skip the predict() method and call directly predictClass()
      Serial.print("Sanity check: ");
      Serial.println(ml.predictClass(x_test));*/
  
      delay(5000);
      ESP.restart();
  }
}
