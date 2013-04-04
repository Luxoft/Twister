/*
File: Panel4.java ; This file is part of Twister.
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
import javax.swing.JTabbedPane;
import java.awt.Dimension;
import java.awt.Toolkit;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.BorderFactory;
import javax.swing.JScrollPane;
import java.awt.FlowLayout;
import javax.swing.border.TitledBorder;
import java.awt.BorderLayout;

public class Panel4 extends JPanel{
    private ConfigFiles config;
    private DBConfig dbconfig;
    private Emails emails;
    private JPanel main; 
    private Plugins plugins;
    private JScrollPane scroll = new JScrollPane();
    private TB tb = new TB();
    private Globals glob;
    private PanicDetect panic;
    private Services services;
    private About about;
    

    public Panel4(){
        setLayout(null);
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        config = new ConfigFiles(screenSize);
        dbconfig = new DBConfig();
        emails = new Emails();
        glob = new Globals();
        panic = new PanicDetect();
        services = new Services();
        plugins = new Plugins();
        about = new About();
        main = new JPanel();        
        main.setLayout(null);
        main.setBounds(240,10,(int)screenSize.getWidth()-320,
                        (int)screenSize.getHeight()-320);
        add(main);   
        RoundButton bpaths = new RoundButton("Paths");
        bpaths.setBounds(20,40,200,25);
        bpaths.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                setPaths();}});
        add(bpaths);  
        RoundButton bemails = new RoundButton("Email");
        bemails.setBounds(20,70,200,25);
        bemails.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                setEmail();}});
        add(bemails);
        RoundButton database = new RoundButton("Database");
        database.setBounds(20,100,200,25);
        database.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                setDatabase();}});
        add(database);
        RoundButton duts = new RoundButton("Test Beds");
        duts.setBounds(20,130,200,25);
        duts.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                setDuts();}});
        add(duts);
        RoundButton globals = new RoundButton("Global Parameters");
        globals.setBounds(20,160,200,25);
        globals.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                setGlobals();}});
        add(globals);
        RoundButton panicb = new RoundButton("Panic Detect");
        panicb.setBounds(20,190,200,25);
        panicb.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){                
                setPanic();}});
        add(panicb);
        RoundButton servicesb = new RoundButton("Services");
        servicesb.setBounds(20,220,200,25);
        servicesb.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){                
                setServices();}});
        add(servicesb);
        RoundButton plugins = new RoundButton("Plugins");
        plugins.setBounds(20,250,200,25);
        plugins.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){                
                setPlugins();}});
        add(plugins);
        RoundButton about = new RoundButton("About");
        about.setBounds(20,280,200,25);
        about.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){                
                setAbout();}});
        add(about);
        setPaths();
    }
    
    /*
     * set about section
     * into this window
     */
    public void setAbout(){
        main.removeAll();
        main.setLayout(new FlowLayout());
        main.add(about);
        main.repaint();
        main.revalidate();}
       
    /*
     * set email content
     * into this window
     */
    public void setEmail(){
        main.removeAll();
        main.setLayout(null);
        scroll = new JScrollPane(emails);
        scroll.setBounds(5,15,main.getWidth()-10,main.getHeight()-20);
        main.add(scroll);
        main.repaint();
        main.revalidate();}
     
    /*
     * set database content
     * into this window
     */
    public void setDatabase(){
        main.removeAll();
        main.setLayout(null);
        scroll = new JScrollPane(dbconfig);
        scroll.setBounds(5,15,main.getWidth()-10,main.getHeight()-20);
        main.add(scroll);
        main.repaint();
        main.revalidate();}
    
    /*
     * set duts  content
     * into this window
     */
    public void setDuts(){        
        main.removeAll();
        main.setLayout(new FlowLayout());
        tb.setPreferredSize(new Dimension(main.getWidth()-5,
                                          main.getHeight()-5));
        main.add(tb);
        main.repaint();
        main.revalidate();}
    
    /*
     * set paths configuration content
     * into this window
     */
    public void setPaths(){
        main.removeAll();
        main.setLayout(null);
        scroll = new JScrollPane(config.paths);
        scroll.getVerticalScrollBar().setUnitIncrement(16);
        scroll.setBounds(5,15,main.getWidth()-10,main.getHeight()-20);
        scroll.getVerticalScrollBar().setValue(0);
        main.add(scroll);
        main.repaint();
        main.revalidate();}
        
        
    /*
     * set services content
     * into this window
     */    
    public void setServices(){
        main.removeAll();
        main.setLayout(new BorderLayout());
        main.add(services,BorderLayout.CENTER);
        scroll = new JScrollPane(services);
        main.add(scroll,BorderLayout.CENTER);
        main.repaint();
        main.revalidate();}
        
    /*
     * set panic detect expressions content
     * into this window
     */
    public void setPanic(){
        main.removeAll();
        main.setLayout(new BorderLayout());
        scroll = new JScrollPane(panic);
        main.add(scroll,BorderLayout.CENTER);
        main.repaint();
        main.revalidate();}
        
     /*
     * set globals content
     * into this window
     */
    public void setGlobals(){
        main.removeAll();
        main.setLayout(new BorderLayout());
        plugins.setPreferredSize(new Dimension(main.getWidth()-5,
                                               main.getHeight()-5));
        main.add(glob.main,BorderLayout.CENTER);
        main.repaint();
        main.revalidate();}
    
    
    /*
     * set plugins  content
     * into this window
     */
    public void setPlugins(){        
        main.removeAll();
        main.setLayout(new FlowLayout());
        plugins.setPreferredSize(new Dimension(main.getWidth()-5,
                                               main.getHeight()-5));
        main.add(plugins);
        main.repaint();
        main.revalidate();}
        
    public Plugins getPlugins(){
        return plugins;}    
    
    public TB getTB(){
        return tb;}
        
    public Emails getEmails(){
        return emails;}
        
    public Services getServices(){
        return services;}
        
    public DBConfig getDBConfig(){
        return dbconfig;}
        
    public ConfigFiles getConfig(){
        return config;}
        
    public Globals getGlobals(){
        return glob;}
    
    public JScrollPane getScroll(){
        return scroll;}
        
    public JPanel getMain(){
        return main;}}
