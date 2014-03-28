/*
File: MainPanel.java ; This file is part of Twister.
Version: 2.009

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
import java.io.File; 
import java.io.PrintStream;
import javax.swing.JOptionPane;
import javax.swing.JTabbedPane;
import java.awt.Dimension;
import java.awt.Toolkit;
import javax.swing.ImageIcon;
import javax.swing.event.ChangeListener;
import javax.swing.event.ChangeEvent;
import java.awt.DefaultKeyboardFocusManager;
import javax.swing.InputMap; 
import javax.swing.JComponent;
import javax.swing.KeyStroke;
import java.awt.event.KeyEvent;
import java.awt.event.InputEvent;
import java.net.URL;
import javax.swing.JScrollPane;
import javax.swing.SwingUtilities;
import javax.swing.JPanel;
import javax.swing.JComboBox;
import java.util.Iterator;

/*
 * twister main container
 * applet - true if starts from applet, false otherwie
 */
public class MainPanel extends JTabbedPane{
    private static final long serialVersionUID = 1L;
    public Panel1 p1;//suites tab
    public Panel2 p2;//masterxml tab
    public Panel4 p4;//configure tab
    public ClearCase p5;
    private boolean applet;
    
    public Panel2 getP2(){
        return p2;
    }
    
    public ClearCase getP5(){
        return p5;
    }

    public MainPanel(boolean applet){
        InputMap map = getInputMap(JComponent.WHEN_ANCESTOR_OF_FOCUSED_COMPONENT);
        KeyStroke keyStroke = KeyStroke.getKeyStroke(KeyEvent.VK_UP,
                                                    InputEvent.CTRL_MASK, false );
        map.put( keyStroke, "DoNothing" );
        RunnerRepository.introscreen.setStatus("Started Main initialization");
        RunnerRepository.introscreen.addPercent(0.035);
        RunnerRepository.introscreen.repaint();
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        this.applet = applet;
        p1 = new Panel1("", applet,(int)screenSize.getWidth());
        p2 = new Panel2(applet);    
        p4 = new Panel4(); 
        setBounds(0, 5, (int)screenSize.getWidth()-50, 672);
        addTab("Project", new ImageIcon(), p1);
        addTab("Reports", null);
        addTab("Configuration", p4); 
        
        /*
         * if it is applet
         * listen for clicks on reports tab
         * and open url when pressed
         */
        if(applet){
            addChangeListener(new ChangeListener(){
                public void stateChanged(ChangeEvent e){
                    if(getSelectedIndex()==1){
                        try{RunnerRepository.applet.getAppletContext().showDocument(
                                                    new URL("http://"+RunnerRepository.host+":"+
                                                    RunnerRepository.getCentralEnginePort()+
                                                    "/report/index/"+RunnerRepository.getUser()), "_blank");}
                        catch(Exception ex){ex.printStackTrace();}
                        setSelectedIndex(0);}}});}
        RunnerRepository.introscreen.setStatus("Finished Main initialization");
        RunnerRepository.introscreen.addPercent(0.035);
        RunnerRepository.introscreen.repaint();
    }
        
    public void saveUserXML(){
        if(!p1.sc.g.getUser().equals("")){
            p1.sc.g.printXML(p1.sc.g.getUser(), false,false,false,false,false,"",false,null,RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefs());}}}
