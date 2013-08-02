/*
File: NetTop.java ; This file is part of Twister.
Version: 2.001

Copyright (C) 2012-2013 , Luxoft

Authors: Andrei Costachi <acostachi@luxoft.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
import javax.swing.JPanel;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.BasicStroke;
import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.Font;
import javax.swing.JLabel;
import javax.swing.ImageIcon;
// import org.apache.xmlrpc.client.XmlRpcClient;
// import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.net.URL;
import java.util.Random;

public class NetTop extends JPanel{
    private String upper = "x";
    private JPanel info;
    private JLabel switch1 = new JLabel("  Switch1",new ImageIcon(Repository.switche2),JLabel.RIGHT);
    private JLabel switch2 = new JLabel("  Switch2",new ImageIcon(Repository.switche2),JLabel.RIGHT);
    private JLabel bar = new JLabel(new ImageIcon(Repository.baricon));
    private SwitchInfo info1,info2,info3,info21,info22,info23;
    
    public NetTop(int width, int height){
        setLayout(null);
        setBackground(Color.WHITE);
        setPreferredSize(new Dimension(1450, 600));
        info = new JPanel();
        info.setBounds(1080, 10, 430, 600);
        info.setBackground(Color.WHITE);
        add(info);
        info.setLayout(null);
        
        switch1.setFont(new Font("TimesRoman", Font.BOLD, 14));
        switch1.setBounds(10,5,250,20);
        info.add(switch1);
        
        bar.setBounds(0,260,325,20);
        info.add(bar);
        
        switch2.setFont(new Font("TimesRoman", Font.BOLD, 14));
        switch2.setBounds(10,295,250,20);
        info.add(switch2);
        
        info1 = new SwitchInfo();
        info1.setBounds(0,25,410,75);
        info.add(info1);
        info1.setIngressport("8");
        info1.setAction("output");
        info1.setOutputPort("18");
        info1.setRxpackets("1028");
        info1.setTxpackets("367");
        info1.setBitrate("4300 ");
        info2 = new SwitchInfo();
        info2.setBounds(0,95,410,75);
        info.add(info2);
        info2.setIngressport("18");
        info2.setAction("output");
        info2.setOutputPort("18");
        info2.setRxpackets("1028");
        info2.setTxpackets("367");
        info2.setBitrate("4300 ");
        info3 = new SwitchInfo();
        info3.setBounds(0,165,410,75);
        info.add(info3);
        info3.setIngressport("34");
        info3.setAction("output");
        info3.setOutputPort("18");
        info3.setRxpackets("1028");
        info3.setTxpackets("367");
        info3.setBitrate("4300 ");
        
        info21 = new SwitchInfo();
        info21.setBounds(0,315,410,75);
        info.add(info21);
        info21.setIngressport("8");
        info21.setAction("output");
        info21.setOutputPort("18");
        info21.setRxpackets("1028");
        info21.setTxpackets("367");
        info21.setBitrate("4300 ");
        info22 = new SwitchInfo();
        info22.setBounds(0,385,410,75);
        info.add(info22);
        info22.setIngressport("18");
        info22.setAction("output");
        info22.setOutputPort("18");
        info22.setRxpackets("1028");
        info22.setTxpackets("367");
        info22.setBitrate("4300 ");
        info23 = new SwitchInfo();
        info23.setBounds(0,455,410,75);
        info.add(info23);
        info23.setIngressport("34");
        info23.setAction("output");
        info23.setOutputPort("18");
        info23.setRxpackets("1028");
        info23.setTxpackets("367");
        info23.setBitrate("4300 ");
        new Thread(){
            public void run(){
                try{
                    String result;
                    String aresult[];
                    while(Repository.run){
                        try{result = Repository.getRPCClient().
                                        execute("ofStatistics",new Object[]{})+"";
                            aresult = result.split(",");
                            switch1.setText("   "+aresult[0]);
                            info1.setIngressport(aresult[1]);
                            info1.setAction(aresult[2]);
                            info1.setOutputPort(aresult[3]);
                            info2.setIngressport(aresult[4]);
                            info2.setAction(aresult[5]);
                            info2.setOutputPort(aresult[6]);
                            info3.setIngressport(aresult[7]);
                            info3.setAction(aresult[8]);
                            info3.setOutputPort(aresult[9]);
                            info1.setRxpackets(aresult[10]);
                            info1.setTxpackets(aresult[11]);
                            info1.setBitrate(aresult[12]);
                            info2.setRxpackets(aresult[13]);
                            info2.setTxpackets(aresult[14]);
                            info2.setBitrate(aresult[15]);
                            info3.setRxpackets(aresult[16]);
                            info3.setTxpackets(aresult[17]);
                            info3.setBitrate(aresult[18]);
                            
                            switch2.setText("   "+aresult[19]);
                            info21.setIngressport(aresult[20]);
                            info21.setAction(aresult[21]);
                            info21.setOutputPort(aresult[22]);
                            info22.setIngressport(aresult[23]);
                            info22.setAction(aresult[24]);
                            info22.setOutputPort(aresult[25]);
                            info23.setIngressport(aresult[26]);
                            info23.setAction(aresult[27]);
                            info23.setOutputPort(aresult[28]);
                            info21.setRxpackets(aresult[29]);
                            info21.setTxpackets(aresult[30]);
                            info21.setBitrate(aresult[31]);
                            info22.setRxpackets(aresult[32]);
                            info22.setTxpackets(aresult[33]);
                            info22.setBitrate(aresult[34]);
                            info23.setRxpackets(aresult[35]);
                            info23.setTxpackets(aresult[36]);
                            info23.setBitrate(aresult[37]);
                            result = Repository.getRPCClient().
                                        execute("ofDataPath",new Object[]{})+"";
                            setUpper(result);
                            try{Thread.sleep(3000);}
                            catch(Exception e){e.printStackTrace();}}
                        catch(Exception e){
                            e.printStackTrace();
                            System.out.println("could not retrieve net info from: "+
                                                "http://"+Repository.host+":"+
                                                Repository.getCentralEnginePort());
                            try{Thread.sleep(3000);}
                            catch(Exception xe){xe.printStackTrace();}}}}
                catch(Exception e){
                    e.printStackTrace();
                    System.out.println("could not retrieve net info from: "+
                                        "http://"+Repository.host+":"+
                                        Repository.getCentralEnginePort());
                    try{Thread.sleep(3000);}
                    catch(Exception ex){ex.printStackTrace();}}}}.start();}
        
    public void paint(Graphics g){
        super.paint(g);
        g.drawImage(Repository.vlcclient, 50, 80, this);
        g.drawImage(Repository.vlcserver, 500, 80, this);
        g.drawImage(Repository.switche, 850, 230, this);  
        g.drawImage(Repository.flootw, 980, 400, this); 
        g.drawImage(Repository.rack150, 25, 410, this);
        g.setFont(new Font("Arial", Font.BOLD, 12));
        g.drawString("OF_Switch_1",20,463);
        g.drawImage(Repository.rack151, 475, 410, this);
        g.drawString("OF_Switch_2",560,463);
        g.drawImage(Repository.rack152, 250, 550, this);
        
        g.setColor(Color.BLUE);
        g.drawLine(850,270,560,270);
        g.drawArc(540,260,20,20,0,180);
        g.drawLine(540,270,110,270);
        g.drawArc(90,260,20,20,0,180);
        g.drawLine(90,270,40,270);
        g.drawLine(40,270,40,435);
        
        g.drawLine(860,275,860,310);
        g.drawLine(860,310,560,310);
        g.drawArc(540,300,20,20,0,180);
        g.drawLine(540,310,490,310);
        g.drawLine(490,310,490,435);
        
        if(upper.equals("d")||upper.equals("x")){
            g.drawLine(870,280,870,505);
            g.drawLine(870,505,260,505);
            g.drawLine(260,505,260,550);}
        else{
            g.drawLine(870,280,870,505);
            g.drawLine(870,505,455,505);
            g.drawArc(435, 495, 20, 20, 0, 180);
            g.drawLine(435,505,260,505);
            g.drawLine(260,505,260,525);
            g.drawArc(250, 525, 20, 15, 270, 180);
            g.drawLine(260,540,260,550);}
        
        g.setColor(new Color(180,180,180));
        g.drawLine(1075,0,1075,getHeight());
        g.setColor(Color.BLACK);
        
        g.drawLine(100, 80, 100, 20);
        g.drawLine(100, 20, 900, 20);
        g.drawLine(900, 20, 900, 260);
        
        g.drawLine(550,80,550,40);
        g.drawLine(550,40,880,40);
        g.drawLine(880,40,880,250);
        
        g.setColor(Color.RED);
        g.drawLine(550,145,550,435);
        
        g.drawLine(100,145,100,435);
        
        g.setColor(Color.BLACK);
        g.drawLine(930,280,1030,280);
        g.drawLine(1030,280,1030,400);
        
        g.setColor(Color.BLUE);
        g.drawLine(30,560,80,560);
        g.setColor(Color.RED);
        g.drawLine(30,575,80,575);
        g.setColor(Color.BLACK);
        g.drawString("management",90,565);
        g.drawString("datapath",90,580);
        g.setFont(new Font("TimesRoman", Font.PLAIN, 14));
        g.drawString("Legend:", 30, 550);
        
        Graphics2D g2D = (Graphics2D)g;
        BasicStroke stroke = new BasicStroke(3);
        g2D.setStroke(stroke);
        g2D.setColor(Color.RED);
        
        if(upper.equals("d")){            
            g2D.drawLine(495,450,495,460);
            g2D.drawLine(495,460,155,460);
            g2D.drawLine(155,460,155,450);}
        else if(upper.equals("c")){
            g2D.drawLine(100,450,290,550);
            g2D.drawLine(550,450,360,550);}}
    
    public void setUpper(String upper){
        this.upper = upper;
        repaint();}}
