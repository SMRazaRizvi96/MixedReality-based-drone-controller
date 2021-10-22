//Do not edit! This file was generated by Unity-ROS MessageGeneration.
using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;
using Unity.Robotics.ROSTCPConnector.MessageGeneration;

namespace RosMessageTypes.DroneControl
{
    [Serializable]
    public class QRPoseMsg : Message
    {
        public const string k_RosMessageName = "drone_control/QRPose";
        public override string RosMessageName => k_RosMessageName;

        public float QR_pos_x;
        public float QR_pos_y;
        public float QR_pos_z;
        public float QR_rot_x;
        public float QR_rot_y;
        public float QR_rot_z;
        public float QR_rot_w;

        public QRPoseMsg()
        {
            this.QR_pos_x = 0.0f;
            this.QR_pos_y = 0.0f;
            this.QR_pos_z = 0.0f;
            this.QR_rot_x = 0.0f;
            this.QR_rot_y = 0.0f;
            this.QR_rot_z = 0.0f;
            this.QR_rot_w = 0.0f;
        }

        public QRPoseMsg(float QR_pos_x, float QR_pos_y, float QR_pos_z, float QR_rot_x, float QR_rot_y, float QR_rot_z, float QR_rot_w)
        {
            this.QR_pos_x = QR_pos_x;
            this.QR_pos_y = QR_pos_y;
            this.QR_pos_z = QR_pos_z;
            this.QR_rot_x = QR_rot_x;
            this.QR_rot_y = QR_rot_y;
            this.QR_rot_z = QR_rot_z;
            this.QR_rot_w = QR_rot_w;
        }

        public static QRPoseMsg Deserialize(MessageDeserializer deserializer) => new QRPoseMsg(deserializer);

        private QRPoseMsg(MessageDeserializer deserializer)
        {
            deserializer.Read(out this.QR_pos_x);
            deserializer.Read(out this.QR_pos_y);
            deserializer.Read(out this.QR_pos_z);
            deserializer.Read(out this.QR_rot_x);
            deserializer.Read(out this.QR_rot_y);
            deserializer.Read(out this.QR_rot_z);
            deserializer.Read(out this.QR_rot_w);
        }

        public override void SerializeTo(MessageSerializer serializer)
        {
            serializer.Write(this.QR_pos_x);
            serializer.Write(this.QR_pos_y);
            serializer.Write(this.QR_pos_z);
            serializer.Write(this.QR_rot_x);
            serializer.Write(this.QR_rot_y);
            serializer.Write(this.QR_rot_z);
            serializer.Write(this.QR_rot_w);
        }

        public override string ToString()
        {
            return "QRPoseMsg: " +
            "\nQR_pos_x: " + QR_pos_x.ToString() +
            "\nQR_pos_y: " + QR_pos_y.ToString() +
            "\nQR_pos_z: " + QR_pos_z.ToString() +
            "\nQR_rot_x: " + QR_rot_x.ToString() +
            "\nQR_rot_y: " + QR_rot_y.ToString() +
            "\nQR_rot_z: " + QR_rot_z.ToString() +
            "\nQR_rot_w: " + QR_rot_w.ToString();
        }

#if UNITY_EDITOR
        [UnityEditor.InitializeOnLoadMethod]
#else
        [UnityEngine.RuntimeInitializeOnLoadMethod]
#endif
        public static void Register()
        {
            MessageRegistry.Register(k_RosMessageName, Deserialize);
        }
    }
}
