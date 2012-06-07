/*
   File: SwitchInfo.java ; This file is part of Twister.

   Copyright (C) 2012 , Luxoft

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
import javax.swing.JLabel;
import java.awt.Color;
import java.awt.Font;
import javax.swing.ImageIcon;

public class SwitchInfo extends JPanel{
    private JLabel ingressport = new JLabel("Ingress_port: ");
    private JLabel tingressport = new JLabel();
    private JLabel action = new JLabel("Action: ");
    private JLabel taction = new JLabel();
    private JLabel outputport = new JLabel("Output_port: ");
    private JLabel packets = new JLabel("Packets ");
    private JLabel toutputport = new JLabel();
    private JLabel rxpackets = new JLabel(" RX: ",new ImageIcon(Repository.inicon),JLabel.LEFT);
    private JLabel txpackets = new JLabel(" TX: ",new ImageIcon(Repository.outicon),JLabel.LEFT);
    private JLabel trxpackets = new JLabel();
    private JLabel ttxpackets = new JLabel();
    private JLabel bitrate = new JLabel("Bitrate: ");
    private JLabel tbitrate = new JLabel();
    
    public SwitchInfo(){
        setLayout(null);
        ingressport.setFont(new Font("Arial",Font.PLAIN,14));
        setBackground(Color.WHITE);
        ingressport.setBounds(5,5,100,20);
        ingressport.setFont(new Font("Arial", Font.BOLD, 12));
        add(ingressport);
        tingressport.setBounds(100,5,90,20);
        tingressport.setFont(new Font("Arial", Font.PLAIN, 12));
        add(tingressport);
        action.setBounds(125,5,60,20);
        action.setFont(new Font("Arial", Font.BOLD, 12));
        add(action);
        taction.setBounds(175,5,80,20);
        taction.setFont(new Font("Arial", Font.PLAIN, 12));
        add(taction);
        outputport.setBounds(235,5,100,20);
        outputport.setFont(new Font("Arial", Font.BOLD, 12));
        add(outputport);
        toutputport.setBounds(325,5,110,20);
        toutputport.setFont(new Font("Arial", Font.PLAIN, 12));
        add(toutputport);
        
        packets.setBounds(15,30,70,20);
        add(packets);
        
        rxpackets.setBounds(120,30,100,20);
        rxpackets.setFont(new Font("Arial", Font.BOLD, 12));
        add(rxpackets);
        trxpackets.setBounds(180,30,80,20);
        trxpackets.setFont(new Font("Arial", Font.PLAIN, 12));
        add(trxpackets);
        txpackets.setBounds(240,30,100,20);
        txpackets.setFont(new Font("Arial", Font.BOLD, 12));
        add(txpackets);
        ttxpackets.setBounds(300,30,80,20);
        ttxpackets.setFont(new Font("Arial", Font.PLAIN, 12));
        add(ttxpackets);
        
        bitrate.setBounds(5,52,60,20);
        bitrate.setFont(new Font("Arial", Font.BOLD, 12));
        add(bitrate);
        tbitrate.setBounds(60,52,70,20);
        tbitrate.setFont(new Font("Arial", Font.PLAIN, 12));
        add(tbitrate);}
        
    public void setIngressport(String port){
        tingressport.setText(port);}
        
    public void setAction(String action){
        taction.setText(action);}
        
    public void setOutputPort(String outputport){
        toutputport.setText(outputport);}
        
    public void setRxpackets(String packets){
        trxpackets.setText(packets);}
        
    public void setTxpackets(String packets){
        ttxpackets.setText(packets);}
        
    public void setBitrate(String packets){
        tbitrate.setText(packets);}}
