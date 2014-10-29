/*
File: TCDetails.java ; This file is part of Twister.
Version: 2.006

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
import javax.swing.JEditorPane;
import java.awt.Font;
import java.awt.Color;
import java.awt.BorderLayout;
import java.awt.Dimension;
import javax.swing.BorderFactory;
import java.awt.event.ActionListener;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import javax.swing.JButton;
import java.io.File;
import javax.swing.JScrollPane;

public class TCDetails extends JPanel{
    public JEditorPane text = new JEditorPane("text/html","");
    private JPanel selector = new JPanel();
    public JButton tcdetails = new JButton("TC details");
    public JButton logs = new JButton("Logs");
    private JPanel p1;
    
    public TCDetails(){
        selector.setPreferredSize(new Dimension(200,35));
        selector.setBackground(Color.WHITE);
        selector.setLayout(null);
        tcdetails.setBounds(2,4,110,30);
        logs.setBounds(116,4,90,30);
        selector.add(tcdetails);
        selector.add(logs);
        setBorder(BorderFactory.createEmptyBorder(15, 10, 5, 10));
        setPreferredSize(new Dimension(450,100));
        setMinimumSize(new Dimension(0,0));
        setMaximumSize(new Dimension(1000,1000));
        setLayout(new BorderLayout());
        text.setEditable(false);        
        text.setCursor(null);  
        text.setOpaque(false);  
        text.setFocusable(false);         
        text.setFont(new Font("Arial",Font.PLAIN,12));
        setBackground(Color.WHITE); 
        text.setBackground(Color.WHITE);
        p1 = new JPanel();
        p1.setLayout(new BorderLayout());
        add(p1,BorderLayout.CENTER);
        JPanel p = new JPanel();
        p.setLayout(new BorderLayout());
        p.add(text,BorderLayout.CENTER);
        JScrollPane sc = new JScrollPane(p);
        p1.add(sc, BorderLayout.CENTER);
        

        add(selector,BorderLayout.SOUTH);
        logs.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                setLogs();
            }
        });
        tcdetails.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                setTCDetails();
            }
        });
    }

    private void setLogs(){
        RunnerRepository.window.mainpanel.getP2().tabbed.removeAll();
            try{
                RunnerRepository.emptyTestRunnerRepository();
                File xml = new File(RunnerRepository.getTestXMLDirectory());    
                int size = RunnerRepository.getLogs().size();
                for(int i=5;i<size;i++){RunnerRepository.getLogs().remove(5);}
                Graphics g=null;
                while(g==null){
                    try{Thread.sleep(100);
                        g = RunnerRepository.window.mainpanel.p1.sc.g.getGraphics();
                        if(g==null)g = RunnerRepository.window.mainpanel.getP2().sc.g.getGraphics();
                    } catch (Exception e){
                        e.printStackTrace();
                    }
                        
                }
                new XMLReader(xml).parseXML(g, true,RunnerRepository.getTestSuite(),false);
                RunnerRepository.window.mainpanel.getP2().updateTabs();
            }
            catch(Exception e){
                e.printStackTrace();
            }
        remove(p1);
        add(RunnerRepository.window.mainpanel.getP2().tabbed,BorderLayout.CENTER);
        revalidate();
        repaint();
    }
    
    public void setTCDetails(){
        remove(RunnerRepository.window.mainpanel.getP2().tabbed);
        add(p1,BorderLayout.CENTER);
        revalidate();
        repaint();
    }
    
}
