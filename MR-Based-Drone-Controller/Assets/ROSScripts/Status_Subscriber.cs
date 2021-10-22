using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
//using RosMessageTypes.DroneControl;
using RosColor = RosMessageTypes.DroneControl.StatusColorMsg;

public class Status_Subscriber : MonoBehaviour
{
    public GameObject circle;

    void Start()
    {
        ROSConnection.instance.Subscribe<RosColor>("status_color", ColorChange);
    }

    void ColorChange(RosColor colorMessage)
    {
        circle.GetComponent<Renderer>().material.color = new Color32((byte)colorMessage.r, (byte)colorMessage.g, (byte)colorMessage.b, (byte)colorMessage.a);
    }
}