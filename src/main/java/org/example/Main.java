package org.example;

import ml.dmlc.xgboost4j.java.Booster;
import ml.dmlc.xgboost4j.java.DMatrix;
import ml.dmlc.xgboost4j.java.XGBoost;
import ml.dmlc.xgboost4j.java.XGBoostError;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws XGBoostError {
        toyCode();
        System.out.println("Hello world!");
    }

    public static void toyCode() throws XGBoostError {
        // Sparse matrix format using CSC (Compressed Sparse Column)
        /*long[] colHeaders = new long[]{0, 2, 4, 7};  // start index of elements in each column
        float[] data = new float[]{1f, 1f, 4f, 2f, 2f, 3f, 3f}; // non-zero data in column-major order
        int[] rowIndex = new int[]{0, 2, 1, 2, 0, 1, 2}; // row indices corresponding to data
        int numRow = 3; // number of rows in the matrix
        DMatrix dmat = new DMatrix(colHeaders, rowIndex, data, DMatrix.SparseType.CSC, numRow);*/

        float[] data = new float[] {1f,2f,3f,4f,5f,6f};
        int nrow = 3;
        int ncol = 2;
        float missing = 0.0f;
        DMatrix dmat = new DMatrix(data, nrow, ncol, missing);

        // Set labels for the training data (necessary for supervised learning)
        float[] labels = new float[]{0.1f, 0.2f, 0.3f}; // example labels for binary classification
        dmat.setLabel(labels);

        // Parameters for the training
        Map<String, Object> params = new HashMap<>();
        params.put("eta", 0.3);
        params.put("max_depth", 3);
        //params.put("objective", "binary:logistic");
        params.put("objective", "reg:squarederror"); // Regression objective


        // Watcher to monitor training progress
        Map<String, DMatrix> watches = new HashMap<>();
        watches.put("train", dmat);

        int numRounds = 100;

        // Training the model
        Booster booster = XGBoost.train(dmat, params, numRounds, watches, null, null);

        // Create a test DMatrix and Predict
        // Ensure to align the number of features (3 columns as per colHeaders implies 3 features)
        float[] testData = new float[]{1.1f, 2.2f};
        DMatrix testMatrix = new DMatrix(testData, 1, 2);
        float[][] predictions = booster.predict(testMatrix);

        System.out.println("Predicted values: " + Arrays.toString(predictions[0]));
    }
}