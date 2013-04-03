/*
File: Window.java ; This file is part of Twister.

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
import java.applet.Applet; 
import javax.swing.JFrame;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.JOptionPane;
import java.io.File;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.awt.Dimension;
import java.awt.Container;
import java.awt.Color;
import javax.swing.JDesktopPane;
import javax.swing.JInternalFrame;
import javax.swing.UIManager;
import java.awt.DefaultKeyboardFocusManager;
import javax.swing.JPanel;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Toolkit;
import javax.swing.JLabel;
import com.twister.CustomDialog;

/*
 * main window displayed if twister is running local
 */
public class Window extends JFrame{
    MainPanel mainpanel;//applet main container
    private static final long serialVersionUID = 1L;
    Applet container;
    JPanel appletpanel;
    
    /*
     * applet - true if starts from applet, false otherwie
     * container - if not null, applet container
     */
   
    public Window(final boolean applet, Applet container){
        this.container = container;
        setTitle("Luxoft - Test Automation Framework");
        Repository.intro.setStatus("Started Frame initialization");
        Repository.intro.addPercent(0.035);
        Repository.intro.repaint();
        mainpanel = new MainPanel(applet);
        if(container!=null){
            appletpanel = new JPanel();
            Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
            appletpanel.setBounds(5, 5, (int)screenSize.getWidth(), 672);
            appletpanel.setBackground(Color.WHITE);
            appletpanel.setLayout(null);
            appletpanel.add(mainpanel);
            container.add(appletpanel);}
        else{
            setLayout(null);
            add(mainpanel);
            String l = null;
            String s = null;
            try{
                l = Repository.getLayouts().get("mainlocation").getAsString();
                s =  Repository.getLayouts().get("mainsize").getAsString();
            } catch(Exception e){
                e.printStackTrace();
            }
            if(l!=null&&s!=null){
                String [] location = l.split(" ");
                String [] size =s.split(" ");
                setBounds((int)Double.parseDouble(location[0]),
                          (int)Double.parseDouble(location[1]),
                          (int)Double.parseDouble(size[0]),
                          (int)Double.parseDouble(size[1]));
            }else{
                setBounds(0,60,mainpanel.getWidth()+30,mainpanel.getHeight()+45);
            }
            
            addWindowListener(new WindowAdapter(){
                public void windowClosing(WindowEvent e){
                    Repository.saveMainLayout();
//                     Repository.uploadPluginsFile();
                    mainpanel.p4.getPlugins().uploadPluginsFile();
                    int r = (Integer)CustomDialog.showDialog(
                                new JLabel("Save your Project XML before exiting ?"),
                                JOptionPane.QUESTION_MESSAGE, 
                                JOptionPane.OK_CANCEL_OPTION, mainpanel, "Save", null);
                    if(r == JOptionPane.OK_OPTION){mainpanel.saveUserXML();}
                    if(deleteTemp(new File(Repository.temp)))
                        System.out.println(Repository.temp+
                                            System.getProperty("file.separator")+
                                            "Twister deleted successfull");
                    else System.out.println("Could not delete: "+Repository.temp+
                                            Repository.getBar()+"Twister");
                    dispose();
                    Repository.run = false;
                    if(!applet)System.exit(0);}});
            addComponentListener(new ComponentAdapter(){
                public void componentResized(ComponentEvent e){
                    if(Repository.window!=null){
                        //mainpanel.p2.splitPane.setSize(getWidth()-52,getHeight()-120);
                        mainpanel.p1.splitPane.setSize(getWidth()-52,getHeight()-120);
                        mainpanel.setSize(getWidth()-28,getHeight()-50);
                        mainpanel.p4.getScroll().setSize(getWidth()-310,getHeight()-150);
                        mainpanel.p4.getMain().setSize(getWidth()-300,getHeight()-130);
                        mainpanel.p4.getTB().setPreferredSize(
                                    new Dimension(getWidth()-300,getHeight()-150));
                        mainpanel.p4.getPlugins().setPreferredSize(
                                    new Dimension(getWidth()-300,getHeight()-150));
                        mainpanel.p4.getPlugins().horizontalsplit.setPreferredSize(
                                    new Dimension(getWidth()-305,getHeight()-155));
                        //mainpanel.p4.getPlugins().setDimension(new Dimension(getWidth()-300,getHeight()-160));                        
                        //Repository.window.mainpanel.p5.nettop.setPreferredSize(new Dimension(getWidth()-50,672));
                    }}});
            setVisible(true);}
        Repository.intro.setStatus("Starting applet");
        Repository.intro.addPercent(1);
        Repository.intro.repaint();
        Repository.intro.dispose();
    }
    
    /*
     * static method used to dele a directory 
     * dir - the directory to be deleted localy
     */
    public static boolean deleteTemp(File dir){    
        if (dir.isDirectory()){
            String[] children = dir.list();
            for (int i=0; i<children.length; i++) {
                boolean success = deleteTemp(new File(dir, children[i])); 
                if(success) System.out.println("successfull");
                else System.out.println("failed");
                if (!success) {return false;}}}
        try{System.out.print("Deleting "+dir.getCanonicalPath()+"....");
            return dir.delete();}
        catch(Exception e){e.printStackTrace();}
        return false;}}