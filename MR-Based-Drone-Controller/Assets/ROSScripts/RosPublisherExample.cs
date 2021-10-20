using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.DroneControl;

/// <summary>
/// 
/// </summary>
public class RosPublisherExample : MonoBehaviour
{
    ROSConnection ros;
    public string topicName = "target_pose";

    // The game object 
    public GameObject goal;
    // Publish the cube's position and rotation every N seconds
    public float publishMessageFrequency = 0.5f;

    // Used to determine how much time has elapsed since the last message was published
    private float timeElapsed;

    void Start()
    {
        // start the ROS connection
        ros = ROSConnection.instance;
        ros.RegisterPublisher<TargetPoseMsg>(topicName);
    }

    private void Update()
    {
        timeElapsed += Time.deltaTime;

        if (timeElapsed > publishMessageFrequency)
        {
            //cube.transform.rotation.x = 0;
            //cube.transform.rotation.z = 0;

            TargetPoseMsg goalPos = new TargetPoseMsg(
                goal.transform.position.x,
                goal.transform.position.y,
                goal.transform.position.z,
                goal.transform.rotation.x,
                goal.transform.rotation.y,
                goal.transform.rotation.z,
                goal.transform.rotation.w
            );

            // Finally send the message to server_endpoint.py running in ROS
            ros.Send(topicName, goalPos);

            timeElapsed = 0;
        }
    }
}
