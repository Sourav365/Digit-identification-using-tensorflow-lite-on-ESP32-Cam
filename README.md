# Digit-identification-using-tensorflow-lite-on-ESP32-Cam
Handwritten digit identification using tensorflow-lite on ESP32 Cam

## Steps:

### 1. Create ML tensorflow model using Pithon code.
Create your own ML model

### 2. Convert tensorflow model to tensorflowLite model for microcontroller.
```
#Convert Keras model to a tflite model

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

#Save the model to disk
open(tflite_model_name + '.tflite', "wb").write(tflite_model)
```

### 3. Copy the c-array file. (".h" file)
```
#Function: Convert some hex value into an array for C programming
def hex_to_c_array(hex_data, var_name):

  c_str = ''

  #Create header guard
  c_str += '#ifndef ' + var_name.upper() + '_H\n'
  c_str += '#define ' + var_name.upper() + '_H\n\n'

  #Add array length at top of file
  c_str += '\nunsigned int ' + var_name + '_len = ' + str(len(hex_data)) + ';\n'

  #Declare C variable
  c_str += 'unsigned char ' + var_name + '[] = {'
  hex_array = []
  for i, val in enumerate(hex_data) :

    #Construct string from hex
    hex_str = format(val, '#04x')

    #Add formatting so each line stays within 80 characters
    if (i + 1) < len(hex_data):
      hex_str += ','
    if (i + 1) % 12 == 0:
      hex_str += '\n '
    hex_array.append(hex_str)

  #Add closing brace
  c_str += '\n ' + format(' '.join(hex_array)) + '\n};\n\n'

  #Close out header guard
  c_str += '#endif //' + var_name.upper() + '_H'

  return c_str
```



```
#Write TFLite model to a C source (or header) file
with open(c_model_name + '.h', 'w') as file:
  file.write(hex_to_c_array(tflite_model, c_model_name))
```
  
### 4. Run Arduino code.
```
#include <EloquentTinyML.h>
#include "digits_model.h"

#define NUMBER_OF_INPUTS 64
#define NUMBER_OF_OUTPUTS 10
// in future projects you may need to tweek this value: it's a trial and error process
#define TENSOR_ARENA_SIZE 8*1024

Eloquent::TinyML::TfLite<NUMBER_OF_INPUTS, NUMBER_OF_OUTPUTS, TENSOR_ARENA_SIZE> ml;


void setup() {
    Serial.begin(115200);
    ml.begin(digits_model);
}

void loop() {
    // pick up a random x and predict its sine
    float x_test[64] = { 0.    , 0.    , 0.625 , 0.875 , 0.5   , 0.0625, 0.    , 0.    ,
                         0.    , 0.125 , 1.    , 0.875 , 0.375 , 0.0625, 0.    , 0.    ,
                         0.    , 0.    , 0.9375, 0.9375, 0.5   , 0.9375, 0.    , 0.    ,
                         0.    , 0.    , 0.3125, 1.    , 1.    , 0.625 , 0.    , 0.    ,
                         0.    , 0.    , 0.75  , 0.9375, 0.9375, 0.75  , 0.    , 0.    ,
                         0.    , 0.25  , 1.    , 0.375 , 0.25  , 1.    , 0.375 , 0.    ,
                         0.    , 0.5   , 1.    , 0.625 , 0.5   , 1.    , 0.5   , 0.    ,
                         0.    , 0.0625, 0.5   , 0.75  , 0.875 , 0.75  , 0.0625, 0.    };
    float y_pred[10] = {0};
    int y_test = 8;

    uint32_t start = micros();

    ml.predict(x_test, y_pred);

    uint32_t timeit = micros() - start;

    Serial.print("It took ");
    Serial.print(timeit);
    Serial.println(" micros to run inference");

    Serial.print("Test output is: ");
    Serial.println(y_test);
    Serial.print("Predicted proba are: ");

    for (int i = 0; i < 10; i++) {
        Serial.print(y_pred[i]);
        Serial.print(i == 9 ? '\n' : ',');
    }

    Serial.print("Predicted class is: ");
    Serial.println(ml.probaToClass(y_pred));
    Serial.print("Sanity check: ");
    Serial.println(ml.predictClass(x_test));

    delay(1000);
}
```



