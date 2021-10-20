using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine;
using System.Collections;
using TMPro;
using Unity.Robotics.ROSTCPConnector;
using QRTracking;
using QRTracking.WindowsMR;
using Microsoft.MixedReality.QR;
using TelloPose = RosMessageTypes.Geometry.PoseMsg;
using System;
using Status = RosMessageTypes.TelloDriver.TelloStatusMsg;


public class VisualizeData : MonoBehaviour
{

    //public TextMeshPro textmeshPro;
    //public TMP_Text textmeshPro;

    public TextMeshProUGUI textmeshPro;
    public GameObject goal;
    public GameObject circle;
    private TelloPose TelloNewPose;
    private UInt16 Battery;




    //public QRCodesVisualizer myVisualizer;

    private string m_label;
    //public string m_label = "Goal x: " + goal.transform.position.x.ToString();

    void Start()
    {
        // textMesh = gameObject.GetComponent<TextMesh>();
        ROSConnection.instance.Subscribe<TelloPose>("/tello/ArucoPose", PoseExtract);
        ROSConnection.instance.Subscribe<Status>("/tello/status", StatusExtract);

    }

    public void PoseExtract(TelloPose obj)
    {
        TelloNewPose = obj;
    }

    public void StatusExtract(Status obj)
    {
        Battery = obj.battery_percentage;
    }

    void Update()
    {

        if (Battery != 0)
        {
            m_label = "Tello Battery Percentage: " + Battery.ToString() + " %\n\n";
            m_label = m_label + "Goal Coordinate =" + "\nx: " + goal.transform.position.x.ToString() + "\ny: " + goal.transform.position.y.ToString() + "\nz: " + goal.transform.position.z.ToString();
        }

        else
        {
            m_label = "Goal Coordinate =" + "\nx: " + goal.transform.position.x.ToString() + "\ny: " + goal.transform.position.y.ToString() + "\nz: " + goal.transform.position.z.ToString();
        }

        //if (myVisualizer.qrCodeObject != null)
        //{
        //  m_label = m_label + "\n\nTello Coordinate =" + "\nx:"  + (myVisualizer.qrCodeObject.transform.position.x + 0.1).ToString() + "\ny: " + (myVisualizer.qrCodeObject.transform.position.y + 0.05).ToString() + "\nz: " + myVisualizer.qrCodeObject.transform.position.z.ToString();
        //}
        //textmeshPro.text = m_label;

        if (TelloNewPose != null)
        {
            m_label = m_label + "\n\nTello Coordinate =" + "\nx: " + (TelloNewPose.position.x).ToString() + "\ny: " + (TelloNewPose.position.y).ToString() + "\nz: " + (TelloNewPose.position.z).ToString();
            if ((Math.Abs(goal.transform.position.x - TelloNewPose.position.x) > 0.1) || (Math.Abs(goal.transform.position.y - TelloNewPose.position.y) > 0.1) || (Math.Abs(goal.transform.position.z - TelloNewPose.position.z) > 0.1))
            {
                circle.GetComponent<Renderer>().material.color = new Color32((byte)255, (byte)0, (byte)0, (byte)255);
            }
            else
            {
                circle.GetComponent<Renderer>().material.color = new Color32((byte)0, (byte)255, (byte)0, (byte)255);
            }
        }
        textmeshPro.text = m_label;
    }
}
