/*
File: Plugins.java ; This file is part of Twister.
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
import java.util.Hashtable;
import java.util.Iterator;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import javax.swing.JCheckBox;
import javax.swing.JTextArea;
import javax.swing.JScrollPane;
import javax.swing.JLabel;
import javax.swing.JButton;
import java.util.Enumeration;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import javax.swing.GroupLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Color;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.Font;
import java.util.ArrayList;
import java.util.Vector;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import javax.swing.JFrame;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.OutputStream;
import java.io.FileOutputStream;
import com.google.gson.JsonArray;
import com.google.gson.JsonPrimitive;
import com.google.gson.JsonObject;
import java.net.URLClassLoader;
import java.util.Arrays;
import javax.swing.JSplitPane;
import java.awt.Color;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import java.net.URLClassLoader;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import java.util.Properties;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.Result;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.OutputKeys;
import java.io.FileInputStream;
import com.twister.Item;

/*
 * plugins panel displayed
 * on configtab when 
 * plugins button is pressed
 */
public class Plugins extends JPanel{
    private Hashtable plugins = new Hashtable(5,0.5f);
    private JScrollPane pluginsscroll;
    private JPanel plugintable, titleborder, downloadtable, localtable, remotetable2;
    public JSplitPane horizontalsplit, verticalsplit;
    private ChannelSftp ch;
    private boolean finished = true;

    public Plugins(){
        initSftp();
        copyPreConfiguredPlugins();
        PluginsLoader.setClassPath();
        getPlugins();
        initComponents();
        loadRemotePluginList();
    }
    
    /*
     * initialize SFTP connection used
     * for plugins and configuration files transfer
     */
    public void initSftp(){
        try{
            JSch jsch = new JSch();
            Session session = jsch.getSession(Repository.user, Repository.host, 22);
            session.setPassword(Repository.password);
            Properties config = new Properties();
            config.put("StrictHostKeyChecking", "no");
            session.setConfig(config);
            session.connect();
            Channel channel = session.openChannel("sftp");
            channel.connect();
            ch = (ChannelSftp)channel;
        } catch (Exception e){
            System.out.println("ERROR: Could not initialize SFTP for plugins");
            e.printStackTrace();
        }
    }
    
    /*
     * method to copy plugins configuration file
     * to server 
     */
    public boolean uploadPluginsFile(){
        try{
            while(!finished){
                try{Thread.sleep(100);}
                catch(Exception e){e.printStackTrace();}
            }
            finished = false;
            DOMSource source = new DOMSource(Repository.getPluginsConfig());
            File file = new File(Repository.PLUGINSLOCALGENERALCONF);
            Result result = new StreamResult(file);
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            transformer.transform(source, result);
            System.out.println("Saving "+file.getName()+" to: "+Repository.USERHOME+"/twister/config/");
            FileInputStream in = new FileInputStream(file);
            ch.cd(Repository.USERHOME+"/twister/config/");
            ch.put(in, file.getName());
            in.close();
            finished = true;
            return true;}
        catch(Exception e){
            e.printStackTrace();
            finished = true;
            return false;
        }
    }
        
    /*
     * loads plugins from
     * PluginsLoader
     */
    public void getPlugins(){
        try{Iterator<TwisterPluginInterface> iterator = PluginsLoader.getPlugins();  
            TwisterPluginInterface plugin=null;
            String name;
            JsonArray pluginsarray;
            int size;
            String pluginname;
            while(iterator.hasNext()){
                try{plugin = iterator.next();}
                catch(Exception e){
                    System.out.println("Could not instatiate plugin");
                    e.printStackTrace();
                    continue;}
                name = plugin.getFileName();
                pluginsarray = Repository.getPlugins().getAsJsonArray();
                size = pluginsarray.size();
                for(int i=0;i<size;i++){
                    pluginname = pluginsarray.get(i).getAsString();
                    if(pluginname.equals(name)&&(plugins.get(pluginname)==null)){
                        plugins.put(pluginname,plugin);
                        break;
                    }
                }
            }}               
        catch(Exception e){
            e.printStackTrace();}
        }
          
    /*
     * Initialize and populate
     * Plugins panel
     */
    public void initComponents(){        
        PluginsLoader.setClassPath();
        titleborder = new JPanel();
        pluginsscroll = new JScrollPane();
        plugintable = new JPanel();
        downloadtable = new JPanel();
        localtable = new JPanel();
        remotetable2 = new JPanel();      
        downloadtable.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createLineBorder(new Color(0, 0, 0)),
                                            "Download"));
        downloadtable.setLayout(new BoxLayout(downloadtable,
                                            BoxLayout.PAGE_AXIS));
        localtable.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createLineBorder(new Color(0, 0, 0)),
                                            "Local"));
        localtable.setLayout(new GridBagLayout());
        remotetable2.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createLineBorder(new Color(0, 0, 0)), "Remote"));
        remotetable2.setLayout(new GridBagLayout());
        titleborder.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createLineBorder(new Color(0, 0, 0)), "Plugins"));
        titleborder.setLayout(new BoxLayout(titleborder, BoxLayout.LINE_AXIS));
        plugintable.setLayout(new GridBagLayout());
        pluginsscroll.setViewportView(plugintable);
        titleborder.add(pluginsscroll);
        verticalsplit = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
                                        new JScrollPane(localtable),
                                        new JScrollPane(remotetable2));
        verticalsplit.setDividerLocation(0.5);
        horizontalsplit = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT,verticalsplit,
                                            new JScrollPane(plugintable));
        horizontalsplit.setDividerLocation(0.5);
        add(horizontalsplit);
        Iterator iterator = plugins.keySet().iterator();
        String name;
        String description;
        while(iterator.hasNext()){
            name = iterator.next().toString();
            TwisterPluginInterface plugin = (TwisterPluginInterface)plugins.get(name);
            description = plugin.getDescription(Repository.PLUGINSDIRECTORY);
            addPlugin(name,description,plugin);}
        JLabel remotedescription = new JLabel("Remote plugins found on server");
        GridBagConstraints gridBagConstraints = new GridBagConstraints();
        gridBagConstraints.anchor = GridBagConstraints.NORTH;
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.ipady = 20;
        remotetable2.add(remotedescription, gridBagConstraints);
        remotedescription = new JLabel("Local installed plugins ");
        gridBagConstraints = new GridBagConstraints();
        gridBagConstraints.anchor = GridBagConstraints.NORTH;
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.ipady = 20;
        localtable.add(remotedescription, gridBagConstraints);
    }            
            
    /*
     * checks plugins defined in .conf
     * and copies the one that are not found
     * localy
     */
    public void copyPreConfiguredPlugins(){
        try{JsonArray plugins = Repository.getPlugins().getAsJsonArray();
            int size = plugins.size();
            String pluginfile;
            File pluginsfolder = new File(Repository.PLUGINSDIRECTORY);
            String [] localplugins = pluginsfolder.list();
            boolean found;
            for(int i=0;i<size;i++){
                pluginfile = plugins.get(i).getAsString();
                found = false;
                for(String file:localplugins){
                    if(file.equals(pluginfile)){
                        File myfile = new File(Repository.PLUGINSDIRECTORY+
                                            Repository.getBar()+pluginfile);
                        try{ch.cd(Repository.REMOTEPLUGINSDIR);}
                        catch(Exception e){
                            System.out.println("Could not get :"+
                                                Repository.REMOTEPLUGINSDIR+
                                                " as remote plugins dir");
                        }
                        try{
                            long remotesize = ch.lstat(pluginfile).getSize();
                            long localsize = myfile.length();
                            if(remotesize==localsize)found = true;
                        }
                        catch(Exception e){
                            e.printStackTrace();
                        }
                        break;}}
                if(!found){
                    copyPlugin(pluginfile);}}}
        catch(Exception e){
            System.out.println("Could not get Plugins Array from local config");
            e.printStackTrace();}}
     
    /*
     * load the list of plugins
     * found on server into this
     * interface
     */
    public void loadRemotePluginList(){        
        String [] downloadedplugins=null;
        File pluginsfile = new File(Repository.PLUGINSDIRECTORY);
        if(pluginsfile.exists())downloadedplugins = pluginsfile.list();   
        ArrayList<String> list = getRemotePlugins();
        JPanel panel;
        JLabel lname;        
        for(String name:list){
            if(name.indexOf(".jar")==-1)continue;
            final String tempname = name;
            lname = new JLabel(name);
            final MyButton addremove = new MyButton("Download");
            addremove.setMyLabel(lname);
            for(String localfile:downloadedplugins){
                if(name.equals(localfile)){
                    JsonArray pluginsarray;
                    String pluginname;
                    pluginsarray = Repository.getPlugins().getAsJsonArray();
                    int size = pluginsarray.size();            
                    for(int i=0;i<size;i++){
                        pluginname = pluginsarray.get(i).getAsString();
                        if(name.equals(pluginname)){
                            addremove.setText("Remove");
                            break;
                        }
                    }
                }
            }
            if(addremove.getText().equals("Remove")){
                GridBagConstraints gridBagConstraints = new GridBagConstraints();
                gridBagConstraints.gridx = 1;
                localtable.add(addremove, gridBagConstraints);
                gridBagConstraints.gridx = 0;
                localtable.add(lname, gridBagConstraints);
                int height = localtable.getComponentCount()*40;                
                localtable.setPreferredSize(new Dimension(240,height));
            }
            else{
                GridBagConstraints gridBagConstraints = new GridBagConstraints();
                gridBagConstraints.gridx = 1;
                remotetable2.add(addremove, gridBagConstraints);
                gridBagConstraints.gridx = 0;
                remotetable2.add(lname, gridBagConstraints);
            }
            addremove.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    addRemovePlugin(addremove,tempname);}});}    
    }
        
        
   /*
    * manages adding or removing plugin
    * based on button press
    */   
    public void addRemovePlugin(MyButton addremove, String filename){
        File pluginfile = new File(Repository.PLUGINSDIRECTORY+
                                    Repository.getBar()+filename);
        if(addremove.getText().equals("Remove")){
            GridBagLayout layout = (GridBagLayout)localtable.getLayout();
            GridBagConstraints constraints = layout.getConstraints(addremove);
            GridBagConstraints constraints1 = layout.getConstraints(addremove.getMyLabel());
            localtable.remove(addremove);
            localtable.remove(addremove.getMyLabel());
            remotetable2.add(addremove,constraints);
            remotetable2.add(addremove.getMyLabel(),constraints1);
            MainPanel main = Repository.window.mainpanel;
            TwisterPluginInterface plugin = ((TwisterPluginInterface)plugins.get(filename));
            if(plugin!=null&&plugin.getContent()!=null){
                try{                    
                    Component comp;
                    for(int i=0;i<main.getTabCount();i++){
                        if(main.getComponentAt(i)==null)continue;
                        try{comp = ((JScrollPane)(main.getComponentAt(i))).getViewport().getView();
                            if(comp == plugin.getContent()){
                                main.removeTabAt(i);
                            }
                        } catch(Exception e){}
                    }                    
                }
                catch(Exception e){
                    System.out.println("There was a problem in removing "+
                        "the plugin with filename: "+filename);
                    e.printStackTrace();
                }
            }
            try{((TwisterPluginInterface)plugins.get(filename)).terminate();}
            catch(Exception e){
                System.out.println("There was a problem in terminatig"+
                    " the plugin with filename: "+filename);
                e.printStackTrace();}
            main.revalidate();
            main.repaint();
            localtable.revalidate();
            localtable.repaint();
            remotetable2.revalidate();
            remotetable2.repaint();
            Repository.removePlugin(filename);
            plugins.remove(filename);
            addremove.setText("Download");
            plugintable.removeAll();
            Iterator iterator = plugins.keySet().iterator();
            String name;
            String description;
            while(iterator.hasNext()){
                name = iterator.next().toString();
                plugin = (TwisterPluginInterface)plugins.get(name);
                description = plugin.getDescription(Repository.PLUGINSDIRECTORY);
                addPlugin(name,description,plugin);}
                plugintable.revalidate();
                plugintable.repaint();
        }
        else{
            if(copyPlugin(filename)){
                addremove.setText("Remove");
                GridBagLayout layout = (GridBagLayout)remotetable2.getLayout();
                GridBagConstraints constraints = layout.getConstraints(addremove);
                GridBagConstraints constraints1 = layout.getConstraints(addremove.getMyLabel());
                remotetable2.remove(addremove);
                remotetable2.remove(addremove.getMyLabel());
                localtable.add(addremove,constraints);
                localtable.add(addremove.getMyLabel(),constraints1);
                localtable.revalidate();
                localtable.repaint();
                remotetable2.revalidate();
                remotetable2.repaint();
                plugintable.removeAll();
                Repository.addPlugin(filename);
                PluginsLoader.setClassPath();
                getPlugins();
                Iterator iterator = plugins.keySet().iterator();
                String name;
                String description;
                while(iterator.hasNext()){
                    name = iterator.next().toString();
                    TwisterPluginInterface plugin = (TwisterPluginInterface)plugins.get(name);
                    description = plugin.getDescription(Repository.PLUGINSDIRECTORY);
                    addPlugin(name,description,plugin);
                }   
            }   
        }
    }
     
    /*
     * method te get plugins from server
     * as an ArrayList
     */
    public ArrayList<String> getRemotePlugins(){
        ArrayList list = new ArrayList<String>();
        Iterator iterator = plugins.keySet().iterator();
        String description;
        try{ch.cd(Repository.REMOTEPLUGINSDIR);}
        catch(Exception e){
            System.out.println("Could not get :"+
                Repository.REMOTEPLUGINSDIR);
            e.printStackTrace();}
        int size;
        try{size= ch.ls(".").size();}
        catch(Exception e){
            System.out.println("No plugins");
            size=0;}
        Vector<LsEntry> plugins = null;
        try{plugins = ch.ls(".");}
        catch(Exception e){
            System.out.println("Error in getting plugins "+
                "from Plugins remote directory");
            e.printStackTrace();}
        if(plugins!=null){
            String name;
            for(int i=0;i<size;i++){                
                name = plugins.get(i).getFilename();
                    if(name.split("\\.").length==0||
                        name.equals("TwisterPluginInterface.jar"))continue;
                    list.add(name);}}
        return list;}
            
    /*
     * method to add plugin 
     * to the downloaded pluginlist
     * @param tname - plugin name to display
     * @param tdescription - plugin descritpion to display
     */
    public void addPlugin(String tname,final String tdescription,
                            TwisterPluginInterface plugin){
        GridBagLayout layout = (GridBagLayout)plugintable.getLayout();
        int componentnr = plugintable.getComponentCount();
        Component component;
        GridBagConstraints constraints;
        if(componentnr>0){
            component = plugintable.getComponent(componentnr-1);
            constraints = layout.getConstraints(component);
            constraints.weightx = 0.1;
            constraints.weighty = 0.1;
            layout.setConstraints(component, constraints);
            component = plugintable.getComponent(componentnr-2);
            constraints = layout.getConstraints(component);
            constraints.weightx = 0.1;
            constraints.weighty = 0.1;
            layout.setConstraints(component, constraints);
            component = plugintable.getComponent(componentnr-3);
            constraints = layout.getConstraints(component);
            constraints.weightx = 0.1;
            constraints.weighty = 0.1;
            layout.setConstraints(component, constraints);
            component = plugintable.getComponent(componentnr-4);
            constraints = layout.getConstraints(component);
            constraints.weightx = 0.1;
            constraints.weighty = 0.1;
            layout.setConstraints(component, constraints);}            
        final MyCheck check = new MyCheck();
        JLabel name = new JLabel();
        JTextArea description = new JTextArea();
        JButton readmore = new JButton("Read more");        
        check.setText("Activate");
        check.setName(tname);
        GridBagConstraints gridBagConstraints = new GridBagConstraints();        
        gridBagConstraints.gridx = 0;
        gridBagConstraints.ipadx = 10;
        gridBagConstraints.ipady = 5;
        gridBagConstraints.anchor = GridBagConstraints.NORTH;
        gridBagConstraints.weightx = 0.1;
        gridBagConstraints.weighty = 25.0;
        plugintable.add(check, gridBagConstraints);
        name.setFont(new java.awt.Font("Tahoma", 1, 11)); 
        name.setText(tname);
        gridBagConstraints = new GridBagConstraints();
        gridBagConstraints.gridx = 1;
        gridBagConstraints.ipadx = 10;
        gridBagConstraints.ipady = 15;
        gridBagConstraints.anchor = GridBagConstraints.NORTH;
        gridBagConstraints.weightx = 0.1;
        gridBagConstraints.weighty = 25.0;
        plugintable.add(name, gridBagConstraints);
        description.setFont(new Font("Monospaced", 0, 14)); 
        description.setEditable(false);
        description.setLineWrap(true);
        description.setTabSize(4);
        if(tdescription.length()<80)description.setText(tdescription);
        else description.setText(tdescription.substring(0, 80)+" ...");
        description.setWrapStyleWord(true);
        description.setAutoscrolls(false);
        description.setMinimumSize(new Dimension(10, 10));
        description.setOpaque(false);
        gridBagConstraints = new GridBagConstraints();
        gridBagConstraints.gridx = 2;
        gridBagConstraints.ipady = 10;
        gridBagConstraints.fill = GridBagConstraints.HORIZONTAL;
        gridBagConstraints.anchor = GridBagConstraints.NORTH;
        gridBagConstraints.weightx = 0.1;
        gridBagConstraints.weighty = 25.0;
        plugintable.add(description, gridBagConstraints);        
        gridBagConstraints = new GridBagConstraints();
        gridBagConstraints.gridx = 3;
        gridBagConstraints.anchor = GridBagConstraints.NORTH;
        gridBagConstraints.weightx = 0.1;
        gridBagConstraints.weighty = 25.0;
        plugintable.add(readmore, gridBagConstraints);        
        readmore.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                showReadMore(tdescription);}});        
        check.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                pluginClicked(check);}});
        if(isPluginEnabled(tname)){
            //wait for MainPanel to be initialized
            new Thread(){
                public void run(){
                    while(Repository.initialized == false){
                        try{Thread.sleep(200);}
                        catch(Exception e){e.printStackTrace();}
                    }
                    String pluginname = check.getName();
                    TwisterPluginInterface plugin = (TwisterPluginInterface)plugins.
                                                    get(pluginname);
                    MainPanel main = Repository.window.mainpanel;
                    
                    Component comp;
                    boolean found = false;
                    for(int i=0;i<main.getTabCount();i++){
                        if(main.getComponentAt(i)==null)continue;
                        try{comp = ((JScrollPane)(main.getComponentAt(i))).getViewport().getView();
                            if(comp == plugin.getContent()){
                                found = true;
                                break;
                            }
                        } catch(Exception e){}
                    }
                    if(!found){check.doClick();
                        
//                     if(main.getComponentZOrder(plugin.getContent())==-1){
//                         check.doClick();
                    }
                    else check.setSelected(true);}
            }.start();
        }
        plugintable.revalidate();
        plugintable.repaint();    
        titleborder.revalidate();
        titleborder.repaint();
    }
        
    /*
     * method to show the readmore window
     * @param description - the description to show
     */
    public void showReadMore(String description){
        JFrame frame = new JFrame("Read More");
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        JTextArea tdescription  = new JTextArea();
        tdescription.setText(description);
        tdescription.setFont(new Font("Monospaced", 0, 14)); 
        tdescription.setEditable(false);
        tdescription.setLineWrap(true);
        tdescription.setTabSize(4);
        tdescription.setWrapStyleWord(true);
        tdescription.setAutoscrolls(false);
        tdescription.setOpaque(false);
        frame.add(new JScrollPane(tdescription));
        frame.setBounds(200,100,800,600);
        frame.setVisible(true);
    }
            
    /*
     * method to display or remove
     * plugin from mainpanel
     */
    public void pluginClicked(final MyCheck check){
        String pluginname = check.getName();
        final TwisterPluginInterface plugin = (TwisterPluginInterface)plugins.get(pluginname);
        final MainPanel main = Repository.window.mainpanel;
        if(check.isSelected()){
            new Thread(){
                public void run(){
                    ArrayList<Item> suites = null; 
                    ArrayList<Item> tests = null;
                    try{suites = Repository.getSuite();}
                    catch(Exception e){e.printStackTrace();}
                    try{tests =  Repository.getTestSuite();}
                    catch(Exception e){e.printStackTrace();}
                    plugin.init(suites,
                        tests,
                        Repository.getVariables(),
                        Repository.getPluginsConfig());
                    main.addTab(plugin.getName(), new JScrollPane(plugin.getContent()));
                    main.revalidate();
                    main.repaint();
                }
            }.start();
        }
        else{
            if(plugin.getContent()!=null){
                try{Component comp;
                    for(int i=0;i<main.getTabCount();i++){
                        if(main.getComponentAt(i)==null)continue;
                        try{comp = ((JScrollPane)(main.getComponentAt(i))).getViewport().getView();
                            if(comp == plugin.getContent()){
                                main.removeTabAt(i);
                            }
                        } catch(Exception e){}
                    }
                }
                catch(Exception e){
                    System.out.println("There was a problem in removing "+
                        "the plugin with filename: "+plugin.getName());
                    e.printStackTrace();
                }
                
                
                //main.remove(plugin.getContent());
                plugin.terminate();
                main.revalidate();
                main.repaint();}
        }
        enablePlugin(check.isSelected(),pluginname);
    }
                
               
    /*
     * deletes plugins found
     * on local plugins directory
     * but not in config file
     */
    public static void deletePlugins(){
        File pluginsdirectory = new File(Repository.PLUGINSDIRECTORY);
        File [] downloadedplugins = pluginsdirectory.listFiles();
        boolean found;
        int size;
        String plugin;
        for(File availableplugin : downloadedplugins ){
            found = false;
            JsonArray plugins= null;
            try{plugins = Repository.getPlugins().getAsJsonArray();}
            catch(Exception e){
                System.out.println("Plugins list from config file is empty ");
                return;}
            size = plugins.size();            
            for(int i=0;i<size;i++){
                plugin = plugins.get(i).getAsString();
//                 if(!availableplugin.getName().equals("Twister.jar") &&
//                     availableplugin.getName().equals(plugin)){
                if( availableplugin.getName().equals(plugin.substring(0,plugin.indexOf("."))+"_description.txt")||
                    availableplugin.getName().equals(plugin)){
                    found = true;
                    break;
                }
            }
            if(!found){
                availableplugin.delete();
            }
        }
    }
    
    /*
     * resize method to be called
     * by window resize
     */
    public void setDimension(Dimension dimension){
        int height = (int)dimension.getHeight();
        titleborder.setPreferredSize(new Dimension(245,height-10));
        titleborder.setMaximumSize(new Dimension(245,height-10));
        titleborder.setMinimumSize(new Dimension(245,height-10));        
        downloadtable.setPreferredSize(new Dimension(245,height));
        downloadtable.setMaximumSize(new Dimension(245,height));
        downloadtable.setMinimumSize(new Dimension(245,height));
    }
           
    /*
     * method to copy plugin jar
     * to local twister plugins directory
     * @param filename- the plugin filename to copy localy
     */
    public boolean copyPlugin(String filename){
        File file = new File(Repository.PLUGINSDIRECTORY+Repository.getBar()+filename);
        InputStream in = null;
        InputStreamReader inputStreamReader = null;
        BufferedReader bufferedReader = null;  
        BufferedWriter writer=null;
        try{
            ch.cd(Repository.REMOTEPLUGINSDIR);
        }
        catch(Exception e){
            System.out.println("Could not get :"+Repository.REMOTEPLUGINSDIR+" as remote plugins dir");
            return false;}
        try{
            //get jar file
            System.out.print("Getting "+filename+" ....");
            in = ch.get(filename);    
            file = new File(Repository.PLUGINSDIRECTORY+Repository.getBar()+filename);
            OutputStream out=new FileOutputStream(file);
            byte buf[]=new byte[100];
            int len;
            while((len=in.read(buf))>0)
                out.write(buf,0,len);
            out.close();
            in.close();
            System.out.println("successfull");
            
            //get plugin description file
            try{
                filename = filename.substring(0, filename.indexOf("."))+"_description.txt";
                System.out.print("Getting "+filename+" ....");
                in = ch.get(filename);    
                file = new File(Repository.PLUGINSDIRECTORY+Repository.getBar()+filename);
                out=new FileOutputStream(file);
                while((len=in.read(buf))>0)
                out.write(buf,0,len);
                out.close();
                in.close();
                System.out.println("successfull");
            } catch(Exception e){e.printStackTrace();}    
            
            return true;}
        catch(Exception e){
            e.printStackTrace();
            System.out.println("Error in copying plugin file " +filename+ " localy");
            return false;}}
                
    public void enablePlugin(boolean value, String filename){
        Document doc = Repository.getPluginsConfig();
        NodeList list1 = doc.getElementsByTagName("Plugin");
        Element item;
        Element compare;
        for(int i=0;i<list1.getLength();i++){
            item = (Element)list1.item(i);
            compare = (Element)item.getElementsByTagName("jarfile").item(0);
            if(compare.getChildNodes().item(0).getNodeValue().equals(filename)){
                compare = (Element)item.getElementsByTagName("status").item(0);
                if(value)compare.getChildNodes().item(0).setNodeValue("enabled");
                else compare.getChildNodes().item(0).setNodeValue("disabled");
                boolean res = uploadPluginsFile();
                return;
            }
        }
    }
                
    /*
     * method to check if plugin with filename
     * is enabled in general plugins config
     */        
    public boolean isPluginEnabled(String filename){
        try{
            Document doc = Repository.getPluginsConfig();
            NodeList list1 = doc.getElementsByTagName("Plugin");
            Element item;
            Element compare;
            for(int i=0;i<list1.getLength();i++){
                item = (Element)list1.item(i);
                compare = (Element)item.getElementsByTagName("jarfile").item(0);
                if(compare.getChildNodes().item(0).getNodeValue().equals(filename)){
                    compare = (Element)item.getElementsByTagName("status").item(0);
                    if(compare.getChildNodes().item(0).getNodeValue().equals("enabled")){
                        return true;
                    }
                    return false;
                }
            }
            return false;}
        catch(Exception e){
            return false;
        }
    }
}
  
/*
 *extended JChecBox to 
 *hold a reference to the
 *plugin name
 */
class MyCheck extends JCheckBox{
    String name;
    
    /*
     * name setter
     */
    public void setName(String name){
        this.name= name;}
    
    /*
     * name getter
     */
    public String getName(){
        return name;}}
        
/*
 *extended JButton to 
 *hold a reference to the
 *filename
 */
class MyButton extends JButton{
    JLabel name;
    
    public MyButton(String name){
        super(name);
    }
    
    /*
     * name setter
     */
    public void setMyLabel(JLabel name){
        this.name= name;}
    
    /*
     * name getter
     */
    public JLabel getMyLabel(){
        return name;}}
