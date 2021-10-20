using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.DroneControl;
//using Microsoft.MixedReality.QR;
using QRTracking;
using TMPro;
using QRTracking.WindowsMR;
using Microsoft.MixedReality.QR;


public class QR_Pose_Publisher_Code : MonoBehaviour
{
    ROSConnection ros;
    public string topicName = "qr_code_pose";

    public QRCodesVisualizer myVisualizer;
    //public SpatialGraphNodeTracker myQRTracker;

    // The game object
    //private GameObject qrCodeCube;
    //public GameObject cube;

    // Publish the qrCodeCube position and rotation every N seconds
    public float publishMessageFrequency = 0.5f;

    //public QRCode myQRCode;


    // Used to determine how much time has elapsed since the last message was published
    private float timeElapsed;

    void Start()
    {
        // start the ROS connection
        ros = ROSConnection.instance;
        ros.RegisterPublisher<QRPoseMsg>(topicName);
        //QRCode.qrCodeCube.transform.localPosition = new Vector3(0.0f, 0.0f, 0.0f);
    }

    private void Update()
    {
        timeElapsed += Time.deltaTime;

        //if (timeElapsed > publishMessageFrequency && QRCode.qrCodeCube != null)
        if (timeElapsed > publishMessageFrequency && myVisualizer.qrCodeObject != null)
        //if (timeElapsed > publishMessageFrequency)
        {

            QRPoseMsg QRPos = new QRPoseMsg(
              //QRCode.qrCodeCube.transform.localPosition[1],
              //QRCode.qrCodeCube.transform.localPosition[2],
              //QRCode.qrCodeCube.transform.localPosition[3]

                //cube.transform.position.x,
                //cube.transform.position.y,
                //cube.transform.position.z
                //myVisualizer.qrCode.transform.position.x,
                //myVisualizer.qrCode.transform.position.y,
                //myVisualizer.qrCode.transform.position.z

                myVisualizer.qrCodeObject.transform.position.x,
                myVisualizer.qrCodeObject.transform.position.y,
                myVisualizer.qrCodeObject.transform.position.z,
                myVisualizer.qrCodeObject.transform.rotation.x,
                myVisualizer.qrCodeObject.transform.rotation.y,
                myVisualizer.qrCodeObject.transform.rotation.z,
                myVisualizer.qrCodeObject.transform.rotation.w

            );

            // Finally send the message to server_endpoint.py running in ROS
            ros.Send(topicName, QRPos);

            timeElapsed = 0;
        }
    }
}