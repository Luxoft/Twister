/*
File: Services.java ; This file is part of Twister.
Version: 2.002

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
import javax.swing.BoxLayout;
import java.awt.Dimension;
import javax.swing.JLabel;
import javax.swing.JButton;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import java.awt.Color;
import javax.swing.BorderFactory;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JFrame;
import java.awt.Point;
import java.awt.BorderLayout;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.Component;
import java.util.ArrayList;
import java.util.Arrays;


public class Services extends JPanel{
    
    public Services(){
        setBorder(BorderFactory.createTitledBorder("Services"));
        setLayout(new BoxLayout(this, BoxLayout.PAGE_AXIS));
        try{
            String result = RunnerRepository.getRPCClient().execute("serviceManagerCommand",
                                                          new Object[]{"list"}).toString();
            String [] services = result.split(",");       
            for(String s:services){
                addNewServices(s);
            }
            revalidate();
            repaint();
        } catch(Exception e){
            e.printStackTrace();
        }
        new Thread(){
            public void run (){
                ArrayList<String> sarray = new<String> ArrayList();
                ArrayList <String>rarray = new<String> ArrayList();
                String [] services;
                while(RunnerRepository.run){
                    try{
                        if(isShowing()){
                            rarray.clear();
                            sarray.clear();
                            for(Component c:getComponents()){
                                rarray.add(((MyPanel)c).getName());
                            }
                            String result = RunnerRepository.getRPCClient().execute("serviceManagerCommand",
                                                                      new Object[]{"list"}).toString();
                            services = result.split(",");
                            for(String c:services){
                                sarray.add(c);
                            }
                            for(String s:sarray){
                                if(!rarray.contains(s)){
                                    addNewServices(s);
                                }
                            }
                            for(String s:rarray){
                                if(!sarray.contains(s)){
                                    for(Component c:getComponents()){
                                        if(((MyPanel)c).getName().equals(s)){
                                            remove(c);
                                        }
                                    }
                                }
                            }
                            revalidate();
                            repaint();
                        }
                        Thread.sleep(2000);}
                    catch(Exception e){e.printStackTrace();}
                    }
            }
        }.start();
    }
    
    private void addNewServices(String name){
        try{
            MyPanel p = new MyPanel(name);
            String result = RunnerRepository.getRPCClient().execute("serviceManagerCommand",
                                                      new Object[]{"description",name}).toString();
            p.setDescription(result);
            result = RunnerRepository.getRPCClient().execute("serviceManagerCommand",
                                                      new Object[]{"status",name}).toString();
            if(result.equals("-1")){
                p.setStatus("running");
            } else {
                p.setStatus("stopped");
            }
            add(p);
        } catch (Exception e){
            e.printStackTrace();
        }
    } 
    
    class MyPanel extends JPanel{
        private static final long serialVersionUID = 1L;
        private String name;
        private JLabel status;
        private JButton start, stop, config;
        private JScrollPane sc;
        private JTextArea desc,conf;
        private JLabel info;
        
        
        public MyPanel(final String name){
            setLayout(null);
            this.name = name;
            setBorder(BorderFactory.createTitledBorder(name));
            setPreferredSize(new Dimension(755, 60));
            setMinimumSize(new Dimension(755, 60));
            setMaximumSize(new Dimension(755, 60));
            status = new JLabel("enabled");
            status.setBounds(335,25,80,20);
            add(status);
            desc = new JTextArea();
            desc.setLineWrap(true);
            desc.setWrapStyleWord(true);
            desc.setEditable(false);
            sc = new JScrollPane(desc);
            sc.setBounds(5,15,300,40);
            add(sc);
            start = new JButton("Start");
            start.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    startService();
                }
            });
            start.setBounds(425,25,80,20);
            add(start);
            if(!PermissionValidator.canEditServices()){
                start.setEnabled(false);
            }
            stop = new JButton("Stop");
            stop.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    stopService();
                }
            });
            stop.setBounds(515,25,80,20);
            add(stop);
            if(!PermissionValidator.canEditServices()){
                stop.setEnabled(false);
            }
            
            config = new JButton("Configuration");
            config.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    configWindow();
                }
            });
            config.setBounds(605,25,140,20);
            add(config);
            if(!PermissionValidator.canEditServices()){
                config.setEnabled(false);
            }
            new Thread(){
                public void run(){
                    while(RunnerRepository.run){
                        try{
                            if(isShowing()){
                                String result = RunnerRepository.getRPCClient().execute("serviceManagerCommand",
                                                                        new Object[]{"status",name}).toString();
                                if(result.equals("-1")){
                                    status.setText("running");
                                    if(PermissionValidator.canEditServices()){
                                        start.setEnabled(false);
                                        stop.setEnabled(true);
                                    }                     
                                } else {
                                    status.setText("stopped");
                                    if(PermissionValidator.canEditServices()){
                                        start.setEnabled(true);
                                        stop.setEnabled(false);
                                    }
                                }
                            }
                            Thread.sleep(1000);}
                        catch(Exception e){e.printStackTrace();}
                    }
                }
            }.start();
        }
        
        public void configWindow(){
            JFrame f = new JFrame(name);
            f.setLayout(new BorderLayout());
            JPanel panel = new JPanel();
            panel.setLayout(new BorderLayout());
            info = new JLabel();
            panel.add(info,BorderLayout.CENTER);
            JButton save = new JButton("Save");
            save.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    saveConf();
                }
            });
            panel.add(save,BorderLayout.EAST);
            Point point = config.getLocationOnScreen();
            f.setAlwaysOnTop(true);
            f.setBounds((int)point.getX()-200,(int)point.getY()-10,300,400);
            f.setVisible(true);
            config.setEnabled(false);
            f.addWindowListener(new WindowAdapter(){
                public void windowClosing(WindowEvent ev){
                    config.setEnabled(true);
                }
            });
            f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
            conf = new JTextArea();
            JScrollPane p = new JScrollPane(conf);
            f.add(p,BorderLayout.CENTER);
            f.add(panel,BorderLayout.SOUTH);
            try{
                conf.setText(RunnerRepository.getRPCClient().execute("serviceManagerCommand",
                                                              new Object[]{"get config",name}).toString());
            } catch(Exception e){
                e.printStackTrace();
            }
        }
        
        private void saveConf(){
            try{
                String result = RunnerRepository.getRPCClient().execute("serviceManagerCommand",
                                                  new Object[]{"set config",name,conf.getText()}).toString();
                info.setText("  "+result);
            } catch(Exception e){
                e.printStackTrace();
            }
        }
        
        public void startService(){
            try{
                String result = RunnerRepository.getRPCClient().execute("serviceManagerCommand",
                                                              new Object[]{"start",name}).toString();
            } catch(Exception e){
                e.printStackTrace();
            }
        }
        
        public void stopService(){
            try{
                String result = RunnerRepository.getRPCClient().execute("serviceManagerCommand",
                                                              new Object[]{"stop",name}).toString();
            } catch(Exception e){
                e.printStackTrace();
            }
        }
        
        public void setStatus(String status){
            this.status.setText(status);
        }
        
        public void setDescription(String desc){
            this.desc.setText(desc);
        }
        
        public String getName(){
            return name;
        }
    }
}
