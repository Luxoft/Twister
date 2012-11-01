/*
File: UnitTesting.java ; This file is part of Twister.

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
import javax.swing.JList;
import javax.swing.JLabel;
import javax.swing.JButton;
import javax.swing.JScrollPane;
import javax.swing.GroupLayout;
import javax.swing.LayoutStyle.ComponentPlacement;
import javax.swing.JFrame;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.text.PlainDocument;
import java.awt.Dimension;
import java.io.File;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.FileReader;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.CardLayout;
import java.util.ArrayList;
import com.twister.Item;
import javax.swing.JOptionPane;
import java.io.InputStreamReader;
import java.io.InputStream;
import java.io.BufferedReader;
import javax.swing.JTextArea;
import javax.swing.JSplitPane;
import javax.swing.BorderFactory;
import sun.misc.BASE64Decoder;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.SwingUtilities;
import javax.swing.JScrollPane;
import javax.swing.text.DefaultCaret;

public class UnitTesting extends JFrame {
    private JButton run;
    private JLabel jLabel1;
    private JList eplist;
    private JScrollPane jScrollPane1;
    private JPanel mainpanel;
    private JTextArea log;
    private JEditTextArea textarea;
    private JSplitPane jPanel1;
    private String todelete;
    private JScrollPane sc;
    private boolean go = true;
    private String logs[] = new String[0];
    private long [] logslength = new long [0];
    private String [] selected = new String[0];
    
    public UnitTesting(String editable, String localfile, String remotefile) {
        initComponents(editable,localfile,remotefile);
        
        String l = null;
        String s = null;
        try{
            l = Repository.getLayouts().get("UTlocation").getAsString();
            s =  Repository.getLayouts().get("UTsize").getAsString();
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
            setBounds(100,100,800,600);
        }
        
        setVisible(true);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        addWindowListener(new WindowAdapter(){
            public void windowClosing(WindowEvent e){
                go = false;
                Repository.saveUTLayout(getSize(),getLocation(),jPanel1.getDividerLocation());
                if(todelete!=null){
                    try{Repository.c.rm(todelete);}
                    catch(Exception ex){
                        System.out.println("Could not delete:"+todelete+" temp file created on server");
                        ex.printStackTrace();
                    }
                }
            }
        });
        readLogs();
    }
    
    private void initComponents(String editable, final String localfile,final String remotefile) {
        mainpanel = new JPanel();
        run = new JButton();
        jLabel1 = new JLabel();
        jScrollPane1 = new JScrollPane();
        eplist = new JList();
        JLabel tcname = new JLabel();
        JLabel desc = new JLabel();
        JTextArea tdesc = new JTextArea();
        try{
            String res = Repository.getRPCClient().execute(
                "getTestDescription", new Object[] { remotefile }).toString();
            System.out.println("RES:"+res);
            String[] cont = res.split("-;-");
            if (cont[1].length() > 1) {
                tdesc.setText(cont[1].substring(1));
            } else {
                tdesc.setText("Not Available");
            }
        } catch(Exception e){
            e.printStackTrace();
            tdesc.setText("Not Available");
        }
        JScrollPane jScrollPane2 = new JScrollPane();
        
        log = new JTextArea();
        ((DefaultCaret)log.getCaret()).setUpdatePolicy(DefaultCaret.ALWAYS_UPDATE);
        log.setEditable(false);
        JPanel p1 = new JPanel();
        p1.setLayout(new CardLayout());
        p1.setBorder(BorderFactory.createTitledBorder("CLI logs"));
        sc = new JScrollPane(log);
        p1.add(sc);
        textarea = new JEditTextArea();
        jPanel1 = new JSplitPane(JSplitPane.VERTICAL_SPLIT,textarea,p1);
        
         try{
            SwingUtilities.invokeLater(new Runnable() {
                public void run() {
                    jPanel1.setDividerLocation(Repository.getLayouts().
                                                 get("UTh1splitlocation").getAsInt());
                }
            });
        } catch(Exception e){
            jPanel1.setDividerLocation(0.2);
        }

        run.setText("Run");

        jLabel1.setText("EP to run on:");
        
        tcname.setText("Test case name: "+editable);
        
        System.out.println("remotefile:"+remotefile);

        desc.setText("Description");
        
        String line = null;                             
        InputStream in = null;
        try{String dir = Repository.getRemoteEpIdDir();
            String [] path = dir.split("/");
            StringBuffer result = new StringBuffer();
            if (path.length > 0) {
                for (int i=0; i<path.length-1; i++){
                    result.append(path[i]);
                    result.append("/");}}
            Repository.c.cd(result.toString());
            in = Repository.c.get(path[path.length-1]);}
        catch(Exception e){e.printStackTrace();};
        InputStreamReader inputStreamReader = new InputStreamReader(in);
        BufferedReader bufferedReader = new BufferedReader(inputStreamReader);  
        StringBuffer b=new StringBuffer("");
        try{while ((line=bufferedReader.readLine())!= null){b.append(line+";");}
            bufferedReader.close();
            inputStreamReader.close();
            in.close();}
        catch(Exception e){e.printStackTrace();}        
        String  [] vecresult = b.toString().split(";");
        eplist.setListData(vecresult);
         tdesc.setEditable(false);
        jScrollPane2.setViewportView(tdesc);
        jScrollPane1.setViewportView(eplist);
        GroupLayout layout = new GroupLayout(mainpanel);
        mainpanel.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 431, Short.MAX_VALUE)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(desc)
                            .addComponent(tcname))
                        .addGap(0, 0, Short.MAX_VALUE)))
                .addGap(18, 18, 18)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jLabel1)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 85, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(run)))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, 335, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(tcname)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(desc)
                    .addComponent(jLabel1))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 0, Short.MAX_VALUE)
                    .addComponent(run, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.PREFERRED_SIZE, 23, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 110, Short.MAX_VALUE))
                .addContainerGap())
        );
        
        run.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                run(remotefile,localfile);    
            }
        });
        add(mainpanel);
        textarea.setFocusTraversalKeysEnabled(false);
        JPopupMenu p = new JPopupMenu();
        JMenuItem item;
        item = new JMenuItem("Copy");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev) {
                textarea.copy();
            }
        });
        p.add(item);
        item = new JMenuItem("Cut");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev) {
                textarea.cut();
            }
        });
        p.add(item);
        item = new JMenuItem("Paste");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev) {
                textarea.paste();
            }
        });
        p.add(item);
        textarea.setRightClickPopup(p);
        textarea.getDocument().putProperty(PlainDocument.tabSizeAttribute, 4);
        if (editable.indexOf(".tcl") != -1) {
            textarea.setTokenMarker(new TCLTokenMarker());
        } else if (editable.indexOf(".py") != -1) {
            textarea.setTokenMarker(new PythonTokenMarker());
        } else if (editable.indexOf(".pl") != -1) {
            textarea.setTokenMarker(new PerlTokenMarker());
        }     
        JButton save = new JButton("Save");
        save.setPreferredSize(new Dimension(70, 20));
        save.setMaximumSize(new Dimension(70, 20));
        final File file = new File(localfile);
        JMenuBar menu = new JMenuBar();
        JMenu filemenu = new JMenu("File");
        JMenuItem saveuser = new JMenuItem("Save");
        saveuser.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev) {
                saveFile(file,remotefile,false);
            }
        });
        filemenu.add(saveuser);
        menu.add(filemenu);
        setJMenuBar(menu);
        File file2 = ExplorerPanel.copyFileLocaly(remotefile, localfile);
        bufferedReader = null;
        try {
            bufferedReader = new BufferedReader(new FileReader(file2));
        } catch (Exception e) {
            e.printStackTrace();
        }
        line = null;
        StringBuffer buf = new StringBuffer();
        try {            
            while ((line = bufferedReader.readLine()) != null) {
                buf.append(line + "\n");
            }
            bufferedReader.close();
        } catch (Exception e) {
            System.out.println("failed to read file localy");
            e.printStackTrace();
        }
        try{
            textarea.setText(buf.toString());
            textarea.setCaretPosition(0);        
        } catch(Exception e){
            e.printStackTrace();
        }
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent ev) {
                if (file.delete()) {
                    System.out.println("File deleted successfully");
                }
                textarea.setText("");
                dispose();
            }
        });
    }
    
    public void run(String remotefile,String localfile){
        ArrayList<Item> items = new ArrayList<Item>();        
        String [] names = remotefile.split("/");       
        names[names.length-1] = "temp_"+names[names.length-1];
        StringBuilder bu = new StringBuilder();
        for(String s:names){
            bu.append(s);
            bu.append("/");
        }
        bu.deleteCharAt(bu.length()-1);
        String tempfile = bu.toString();
        
        Item parent = new Item("temp",2, -1, 5, 0,0 , null);
        Item test = new Item(tempfile,1, -1, 5, 0,0 , null);
        
        parent.addSubItem(test);        
        selected = new String[eplist.getSelectedValuesList().size()];
        for(int i=0;i<eplist.getSelectedValuesList().size();i++){
            selected[i] = eplist.getSelectedValuesList().get(i).toString();
        }
        if(selected.length == 0){
            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Repository.window,
                                            "Warning","Please select at least one EP to run on");
            return;
        }
        parent.setEpId(selected);
        items.add(parent);
        XMLBuilder xml = new XMLBuilder(items);
        xml.createXML(false,false,true,"","",false,"");
        String dir = Repository.getXMLRemoteDir();
        String [] path = dir.split("/");
        StringBuffer result2 = new StringBuffer();
        if (path.length > 0){
            for (int i=0; i<path.length-1; i++){
                result2.append(path[i]);
                result2.append("/");}}
        final String filelocation = result2.toString()+"testsuites_temp.xml";
        if(!xml.writeXMLFile("testsuites_temp.xml", false,true)){
            System.out.println("Could not write testsuites_temp.xml");
            return;
        }
        saveFile(new File(localfile),tempfile,true);
        new Thread(){
            public void run(){
                try{
                    String result = Repository.getRPCClient().execute("runTemporary",
                                                        new Object[]{Repository.getUser(),
                                                                    filelocation})+"";
                    if(result.indexOf("ERROR")!=-1){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                              UnitTesting.this, "Failed", 
                                              result);
                    }
                }
                catch(Exception e){
                    e.printStackTrace();
                }
            }
        }.start();
    }
    
    public void readLogs(){
        new Thread(){
            public void run(){
                boolean update = false;
                while(go){
                    try{
                        update = false;
                        if(selected.length != logs.length){
                            logs = new String[selected.length];
                            logslength = new long[selected.length];
                        }
                        String result;
                        long resp;
                        for(int i=0;i<selected.length;i++){
                            result = Repository.getRPCClient().execute("getLogFile",
                                                                        new Object[]{Repository.getUser(),
                                                                                     "0","0",selected[i]+"_CLI.log"})+"";
                            resp = Long.parseLong(result);
                            if(logslength[i]!=resp){
                                logslength[i] = resp;
                                logs[i] = Repository.getRPCClient().execute("getLogFile",
                                                                  new Object[]{Repository.getUser(),
                                                                  "1","0",selected[i]+"_CLI.log"})+"";
                                update = true;
                            }
                        }
                        if(update){
                            log.setText("");
                            for(int i=0;i<logs.length;i++){
                                log.append(selected[i]+" log"+"\n\n"+readText(logs[i]));
                            }
                        }
                        Thread.sleep(1000);
                    }
                    catch(Exception e){
                        e.printStackTrace();
                    }
                }
            }
        }.start(); 
    }
    
    public void saveFile(File file,String remotefile,boolean overwrite){
        try{
            FileWriter filewriter = new FileWriter(file);
            BufferedWriter out = new BufferedWriter(filewriter);
            out.write(textarea.getText());
            out.flush();
            out.close();
            filewriter.close();
            ExplorerPanel.sendFileToServer(file, remotefile);
            if(overwrite)todelete = remotefile;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public String readText(String content){
        BASE64Decoder base64 = new BASE64Decoder();
        byte mydata[]=null;
        try{mydata = base64.decodeBuffer(content);}
        catch(Exception e){e.printStackTrace();}
        return (new String(mydata));}
}