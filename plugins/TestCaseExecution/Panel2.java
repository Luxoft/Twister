/*
File: Panel2.java ; This file is part of Twister.
Version: 2.0014

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
import com.twister.Item;
import java.io.File;
import java.io.PrintStream;
import javax.swing.JPanel;
import javax.swing.JButton;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.IOException;
import javax.swing.ImageIcon;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.BorderFactory;
import javax.swing.JSplitPane;
import java.awt.Dimension;
import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeEvent;
import java.net.URL;
import java.net.URLConnection;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import javax.swing.JTabbedPane;
import java.util.ArrayList;
import java.net.URL;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import java.awt.Toolkit;
import java.io.FileInputStream;
import java.io.FileWriter;
import javax.swing.JFileChooser;
import javax.swing.JLabel;
import java.awt.Color;
import javax.swing.JOptionPane;
import javax.swing.JFrame;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import jxl.write.Label;
import jxl.write.WritableWorkbook;
import jxl.write.WritableSheet;
import java.io.File;
import jxl.Workbook;
import jxl.CellView;
import javax.swing.SwingUtilities;
import com.twister.CustomDialog;

public class Panel2 extends JPanel{
    private static final long serialVersionUID = 1L;
    public ScrollGraficTest sc;
    ArrayList<Log> logs=new ArrayList<Log>();
    JSplitPane splitPane;
    public JTabbedPane tabbed;
    private boolean cleared = true;
    public JLabel cestatus;
    private boolean stoppushed = false;
    private boolean runned = false;
    public JButton stop,play;
    private boolean first = true;
    private boolean savedb;

    public Panel2(final boolean applet){
        RunnerRepository.introscreen.setStatus("Started Monitoring interface initialization");
        RunnerRepository.introscreen.addPercent(0.035);
        RunnerRepository.introscreen.repaint();
        init(applet);
        tabbed = new JTabbedPane();
        setLayout(null);
        play = new JButton("Run",new ImageIcon(RunnerRepository.getPlayIcon()));
        play.setEnabled(false);
        play.setBounds(80,20,105,25);
        play.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                play(play);}});
        add(play);
        stop = new JButton("Stop",new ImageIcon(RunnerRepository.getStopIcon()));
        stop.setEnabled(false);
        stop.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                stop(play);}});
        stop.setBounds(190,20,95,25);
        add(stop);
        cestatus = new JLabel("CE status: ");
        cestatus.setBounds(290,25,650,25);
        cestatus.setForeground(new Color(100,100,100));
        add(cestatus);
        try{new Thread(){
                public void run(){
                    while(RunnerRepository.run){ 
                        askCE(play);}}}.start();}
        catch(Exception e){e.printStackTrace();}
        RunnerRepository.introscreen.setStatus("Finished Monitoring interface initialization");
        RunnerRepository.introscreen.addPercent(0.035);
        RunnerRepository.introscreen.repaint();
    }
    
    //methods used to refresh
    //the panel
    public void init(boolean applet){
        sc = new ScrollGraficTest(0, 0,applet);
    }
        
    /*
     * get status from ce
     * and adjust accordingly
     */
    private void askCE(JButton play){
        try{String result;
            Thread.sleep(1000);
            result = RunnerRepository.getRPCClient().execute("getExecStatusAll",new Object[]{RunnerRepository.getUser()})+" ";
            String startedtime = "   Started : "+result.split(";")[1];
            String elapsedtime = "   Elapsed time: "+result.split(";")[2];
            String user = "   Started by: "+result.split(";")[3];
            result = result.split(";")[0];
            if(result.equals("paused")){
                RunnerRepository.window.mainpanel.p1.setGenerate(false);
                cestatus.setText("CE status: paused"+startedtime+elapsedtime+user);
                cleared=false;
                play.setText("Resume");
                play.setIcon(new ImageIcon(RunnerRepository.playicon));
                if(first){
                    RunnerRepository.window.mainpanel.p1.setRunning();
                    first = false;
                }
            }
            else if(result.equals("stopped")){
                if(first){
                    while(!RunnerRepository.initialized){
                        try{Thread.sleep(1000);}
                        catch(Exception ex){
                            ex.printStackTrace();
                        }
                    }
                    RunnerRepository.openProjectFile();
                    first = false;
                }
                RunnerRepository.window.mainpanel.p1.setGenerate(true);
                cestatus.setText("CE status: stopped");
                stop.setEnabled(false);
                RunnerRepository.window.mainpanel.p1.edit.setEnabled(true);
                play.setText("Run");
                play.setIcon(new ImageIcon(RunnerRepository.playicon));
                if(runned && !savedb){
                    new Thread(){
                        public void run(){
                            try{
                                Thread.sleep(200);
                                userOptions();
                            } catch(Exception e){
                                e.printStackTrace();
                            }
                        }
                    }.start();
                    runned = false;
                }
                stoppushed = false;}
            else if(result.equals("running")){
                
                if(first){
                    while(!RunnerRepository.initialized){
                        try{Thread.sleep(1000);}
                        catch(Exception ex){
                            ex.printStackTrace();
                        }
                    }
                    first = false;
                    RunnerRepository.window.mainpanel.p1.setGenerate(false);
                    stoppushed = false;
                    runned = true;
                    cestatus.setText("CE status: running"+startedtime+elapsedtime+user);
                    stop.setEnabled(true);
                    RunnerRepository.window.mainpanel.p1.edit.setEnabled(false);
                    cleared=false;
                    play.setText("Pause");
                    play.setIcon(new ImageIcon(RunnerRepository.pauseicon));
                    RunnerRepository.window.mainpanel.p1.setRunning();
                } else {
                    RunnerRepository.window.mainpanel.p1.setGenerate(false);
                    stoppushed = false;
                    runned = true;
                    cestatus.setText("CE status: running"+startedtime+elapsedtime+user);
                    stop.setEnabled(true);
                    RunnerRepository.window.mainpanel.p1.edit.setEnabled(false);
                    cleared=false;
                    play.setText("Pause");
                    play.setIcon(new ImageIcon(RunnerRepository.pauseicon));
                }
                RunnerRepository.window.mainpanel.p1.setGenerate(false);
                stoppushed = false;
                runned = true;
                cestatus.setText("CE status: running"+startedtime+elapsedtime+user);
                stop.setEnabled(true);
                RunnerRepository.window.mainpanel.p1.edit.setEnabled(false);
                cleared=false;
                play.setText("Pause");
                play.setIcon(new ImageIcon(RunnerRepository.pauseicon));
            }
            if(!play.isEnabled()){
                play.setEnabled(true);
                stop.setEnabled(true);
                RunnerRepository.window.mainpanel.p1.edit.setEnabled(false);
            }
            Object result1 = RunnerRepository.getRPCClient().execute("getFileStatusAll",
                                                                new Object[]{RunnerRepository.getUser()});
            if(result1!=null){                                    
                if(((String)result1).indexOf(",")!=-1){
                    String[] result2 = ((String)result1).split(",");
                    updateStatuses(result2);}
                else{
                    String[] result2 = {(String)result1};
                    updateStatuses(result2);}}
//                     }
            }
        catch(Exception e){
            e.printStackTrace();
            if(first){
                while(!RunnerRepository.initialized){
                    try{Thread.sleep(1000);}
                    catch(Exception ex){
                        ex.printStackTrace();
                    }
                }
                RunnerRepository.openProjectFile();
                first = false;
            }
            try{Thread.sleep(1000);}
            catch(Exception ex){
                ex.printStackTrace();
            }
            System.out.println("Could not connect to: "+RunnerRepository.host+" on port"+
                                RunnerRepository.getCentralEnginePort());
                                
            e.printStackTrace();
            
            if(play.isEnabled()){
                play.setEnabled(false);
                stop.setEnabled(false);
                RunnerRepository.window.mainpanel.p1.edit.setEnabled(true);
            }}}
                
    /*
     * Prompt user to save to db or
     * localy in excel file
     */           
    private void userOptions(){
        String[] buttons = {"Save to DB","Export to excel","Cancel"};
        String resp = CustomDialog.showButtons(Panel2.this, JOptionPane.QUESTION_MESSAGE,
                                                JOptionPane.DEFAULT_OPTION, null,buttons ,
                                                "Confirmation","Generate statistics?");
        if (!resp.equals("NULL")) {
            if(resp.equals("Save to DB")){
                System.out.println("Saving to DB");
                try{RunnerRepository.getRPCClient().execute("commitToDatabase",
                                                      new Object[]{RunnerRepository.getUser()});}
                catch(Exception e){
                    System.out.println("Could not comunicate with ce through RPC");
                    e.printStackTrace();}}
            else if(resp.equals("Export to excel")){
                System.out.println("Exporting to excel..");
                generateExcel();}}
        if(!stoppushed){
            System.out.println("Without stop button");}}
    
    /*
     * stop CE from executing
     */
    public void stop(JButton play){
        try{String status = (String)RunnerRepository.getRPCClient().execute("setExecStatusAll",
                                                                      new Object[]{RunnerRepository.getUser(),0});
            play.setText("Run");
            play.setIcon(new ImageIcon(RunnerRepository.playicon));
            stoppushed = true;}
        catch(Exception e){e.printStackTrace();}}
    
    /*
     * Handle play button pressed based on
     * play previous status
     */
    public void play(JButton play){
        try{String status="";
            if(play.getText().equals("Run")){
                for(int i=0;i<RunnerRepository.getTestSuiteNr();i++){clearProp(RunnerRepository.getTestSuita(i));}
                RunnerRepository.window.mainpanel.getP2().sc.g.repaint();    
                status = (String)RunnerRepository.getRPCClient().execute("setExecStatusAll",
                                                                    new Object[]{RunnerRepository.getUser(),2});
                String [] path = RunnerRepository.window.mainpanel.p1.sc.g.getUser().split("\\\\");
                String file = path[path.length-1];
                RunnerRepository.getRPCClient().execute("setStartedBy",
                                                    new Object[]{RunnerRepository.getUser(),
                                                                 RunnerRepository.getUser()+";"+file});
                play.setText("Pause");
                play.setIcon(new ImageIcon(RunnerRepository.pauseicon));}
            else if(play.getText().equals("Resume")){
                status = (String)RunnerRepository.getRPCClient().execute("setExecStatusAll",
                                                                    new Object[]{RunnerRepository.getUser(),3});
                play.setText("Pause");
                play.setIcon(new ImageIcon(RunnerRepository.playicon));}
            else if(play.getText().equals("Pause")){
                status = (String)RunnerRepository.getRPCClient().execute("setExecStatusAll",new Object[]{RunnerRepository.getUser(),1});
                play.setText("Resume");
                play.setIcon(new ImageIcon(RunnerRepository.playicon));}}
        catch(Exception e){e.printStackTrace();}}
    
    /*
     * Ask and generate excel file
     * with the suites and their status
     */
    public boolean generateExcel(){   
        try{JFileChooser chooser = new JFileChooser(); 
            chooser.setApproveButtonText("Save");
            chooser.setCurrentDirectory(new java.io.File("."));
            chooser.setDialogTitle("Choose Location");         
            chooser.setAcceptAllFileFilterUsed(false);    
            if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
                WritableWorkbook workbook = Workbook.createWorkbook(new File(chooser.getSelectedFile()+
                                                                                                ".xls")); 
                WritableSheet sheet = workbook.createSheet("First Sheet",0);
                int columns = 4+RunnerRepository.getTestSuita(0).getUserDefNr();
                Label label;
                String titles []= new String[columns];
                titles[0] = "Suite";
                titles[1] = "TC";
                titles[2] = "EPId";
                titles[3] = "Status";
                for(int i=4;i<columns;i++){
                    titles[i]=RunnerRepository.getTestSuita(0).getUserDef(i-4)[0];}
                for(int i=0;i<columns;i++){
                    label = new Label(i, 0, titles[i]);
                    sheet.addCell(label);}
                int index = 1;
                for(int i=0;i<RunnerRepository.getTestSuiteNr();i++){
                    Item suita = RunnerRepository.getTestSuita(i);
                    index = addToExcel(sheet,suita,index,columns);}
                CellView view = new CellView();
                view.setAutosize(true);
                for(int i=0;i<columns;i++)sheet.setColumnView(i,view);
                sheet.getSettings().setVerticalFreeze(1);
                workbook.write();
                workbook.close();
                return false;}
            else {System.out.println("No Selection");
                return false;}}
        catch(Exception e){
            System.out.println("There was a problem in writing excel file,"+
                                        " make sure file it is not in use.");
            e.printStackTrace();
            boolean continua = true;
            while(continua){
                continua = generateExcel();
                if(!continua)return continua;}
            return false;}}
        
    /*
     * method to populate excel row 
     * with suites data
     * 
     * sheet - excel sheet to be populated
     * element - the Item to populate excel data with
     * index - row numbel
     * columns - the columns to populate
     */
    public int addToExcel(WritableSheet sheet,Item element,int index,int columns){
        if(element.getType()==1){
            Label label;
            try{label = new Label(0, index,Grafic.getFirstSuitaParent(element,true).getName());                
                sheet.addCell(label);
                label = new Label(1, index,element.getName());                
                sheet.addCell(label);
                StringBuilder s = new StringBuilder();
                for(String g:Grafic.getFirstSuitaParent(element,true).getEpId()){
                    s.append(g+";");
                }
                s.deleteCharAt(s.length()-1);
                label = new Label(2, index, s.toString());                
                sheet.addCell(label);
                label = new Label(3, index,element.getSubItem(0).getValue());
                sheet.addCell(label);
                for(int i=4;i<columns;i++){
                    label = new Label(i, index,Grafic.getParent(element, true).getUserDef(i-4)[1]);
                    sheet.addCell(label);}
                index++;}
            catch(Exception e){
                System.out.println("Could not write to excel sheet");
                e.printStackTrace();}
            return index;}
        else if(element.getType()==2){
            for(int i=0;i<element.getSubItemsNr();i++){
                index = addToExcel(sheet,element.getSubItem(i),index,columns);}
            return index;}
        return index;}
   
    /*
     * Update tabs based on
     * the logs found in RunnerRepository
     */
    public void updateTabs(){
        tabbed.removeAll();
        logs.clear();
        SwingUtilities.invokeLater(new Runnable() { 
          public void run(){
            try{for(int i=0;i<RunnerRepository.getLogs().size();i++){
                    if(i==4)continue;
                    if(RunnerRepository.getLogs().get(i).equals(""))continue;
                    Log log = new Log(RunnerRepository.getLogs().get(i));
                    logs.add(log);
                    tabbed.addTab(RunnerRepository.getLogs().get(i),log.container);
                }
                Log log = new Log("server_log");
                log.clearlog.setEnabled(false);
                logs.add(log);
                tabbed.addTab("server_log",log.container);
            }
            catch(Exception e){e.printStackTrace();}}});
        TabsReorder.enableReordering(tabbed);} 

    /*
     * update TC satatus
     */
    public void updateStatuses(String [] statuses){
        int index = 0;
        updateSummary(statuses);
        for(int i=0;i<RunnerRepository.getTestSuiteNr();i++){
            index = manageSubchildren(RunnerRepository.getTestSuita(i),statuses,index);}
            RunnerRepository.window.mainpanel.getP2().sc.g.repaint();}
            
    public void updateSummary(String [] stats){
        int [] val = new int[10];
        val[0] = stats.length;
        for(String s:stats){
            if(s.equals("10")||s.equals("-1"))val[1]++;
            else if(s.equals("1"))val[2]++;
            else if(s.equals("2"))val[3]++;
            else if(s.equals("3"))val[4]++;
            else if(s.equals("4"))val[5]++;
            else if(s.equals("5"))val[6]++;
            else if(s.equals("6"))val[7]++;
            else if(s.equals("7")||s.equals("8")){
                val[8]++;}
            else if(s.equals("9"))val[9]++;
        }
        RunnerRepository.window.mainpanel.p1.suitaDetails.updateStats(val);
    }
    
    /*
     * interpret status value
     * and asign it to item
     */
    public int manageSubchildren(Item item, String[]statuses, int index){
        int index2 = index;
        if(item.getType()==1&&statuses.length>index2){
            if(statuses[index2].equals("10")||statuses[index2].equals("-1"))item.getSubItem(0).setValue("pending");
            else if(statuses[index2].equals("1"))item.getSubItem(0).setValue("running");
            else if(statuses[index2].equals("2"))item.getSubItem(0).setValue("pass");
            else if(statuses[index2].equals("3"))item.getSubItem(0).setValue("fail");
            else if(statuses[index2].equals("4"))item.getSubItem(0).setValue("skipped");
            else if(statuses[index2].equals("5"))item.getSubItem(0).setValue("aborted");
            else if(statuses[index2].equals("6"))item.getSubItem(0).setValue("not executed");
            else if(statuses[index2].equals("7"))item.getSubItem(0).setValue("timeout");
            else if(statuses[index2].equals("8"))item.getSubItem(0).setValue("invalid");
//             else if(statuses[index2].equals("7")||statuses[index2].equals("8")){
//                 item.getSubItem(0).setValue("timeout");}
            else if(statuses[index2].equals("9"))item.getSubItem(0).setValue("waiting");
            index2++;
            return index2;}
        else if(item.getType()==2){
            for(int i=0;i<item.getSubItemsNr();i++){                
                index2 = manageSubchildren(item.getSubItem(i),statuses,index2);}
            return index2;}
        return index2;}
        
    public void setSaveDB(boolean savedb){
        this.savedb = savedb;
    }
     
    /*
     * return status of stop button
     */
    public boolean getStopStatus(){
        return stop.isEnabled();}
            
    /*
     * assign value Pending to item
     */
    public void clearProp(Item item){
        if(item.getType()==1)item.getSubItem(0).setValue("Pending");
        else if (item.getType()==2){
            for(int i=0;i<item.getSubItemsNr();i++){clearProp(item.getSubItem(i));}}}}
