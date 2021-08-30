using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine;
using System.Collections;
using TMPro;
using QRTracking;
using QRTracking.WindowsMR;
using Microsoft.MixedReality.QR;

public class VisualizeData : MonoBehaviour
{

    //public TextMeshPro textmeshPro;
    //public TMP_Text textmeshPro;

    public TextMeshProUGUI textmeshPro;
    public GameObject goal;
    public QRCodesVisualizer myVisualizer;

    private string m_label;
    //public string m_label = "Goal x: " + goal.transform.position.x.ToString();

    void Start()
    {
        // textMesh = gameObject.GetComponent<TextMesh>();
    }

    void Update()
    {
        m_label = "Goal Coordinate =" + "\nx: " + goal.transform.position.x.ToString() + "\ny: " + goal.transform.position.y.ToString() + "\nz: " + goal.transform.position.z.ToString();
        if (myVisualizer.qrCodeObject != null)
        {
            m_label = m_label + "\n\nTello Coordinate =" + "\nx:"  + (myVisualizer.qrCodeObject.transform.position.x + 0.1).ToString() + "\ny: " + (myVisualizer.qrCodeObject.transform.position.y + 0.05).ToString() + "\nz: " + myVisualizer.qrCodeObject.transform.position.z.ToString();
        }
        textmeshPro.text = m_label;

        //TextMeshPro textmeshPro = GetComponent<TextMeshPro>();

        //textmeshPro.SetText("The first number is {0} and the 2nd is {1:2} and the 3rd is {3:0}.", 4, 6.345f, 3.5f);
        // The text displayed will be:
        // The first number is 4 and the 2nd is 6.35 and the 3rd is 4.
    }
}
