/*
File: applet.java ; This file is part of Twister.

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
import java.util.ArrayList;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import com.jcraft.jsch.JSchException;
import java.io.File;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.ByteArrayOutputStream;
import java.io.OutputStream;
import java.io.FileOutputStream;
import java.util.Properties;
import java.awt.Image;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import javax.xml.parsers.ParserConfigurationException;
import org.xml.sax.SAXException;
import java.io.IOException;
import java.util.Arrays;
import javax.swing.JTextField;
import javax.swing.JPasswordField;
import javax.swing.JOptionPane;
import javax.swing.tree.DefaultMutableTreeNode;
import java.net.URL;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import com.google.gson.JsonParser;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;
import java.util.Iterator;
import java.util.Map.Entry;
import com.google.gson.JsonPrimitive;
import java.io.Writer;
import java.io.OutputStreamWriter;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import javax.swing.JDialog;
import javax.swing.JPanel;
import java.awt.Color;
import javax.swing.BoxLayout;
import javax.swing.JLabel;
import java.awt.BorderLayout;
import javax.swing.JComboBox;
import javax.swing.JCheckBox;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.UIManager;
import javax.swing.SwingUtilities;
import java.awt.Dimension;
import java.util.Vector;
import java.util.Hashtable;
import com.twister.Item;
import javax.xml.transform.Result;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;

/*
 * static class to hold
 * twister resources
 */
public class Repository{
    private static ArrayList <Item> suite = new ArrayList <Item> ();//suite list
    private static ArrayList<Item> suitetest = new ArrayList<Item>();//test suite list generated
    private static String bar = System.getProperty("file.separator");//System specific file.separator
    private static ArrayList<String> logs = new ArrayList<String>();//logs tracked by twister framwork
    public static String[] columnNames;
    public static Window window;//main window displayed if twister is running local
    public static ChannelSftp c;//main sftp connection used by Twister
    public static Hashtable variables = new Hashtable(5,0.5f);
    public static String user,host,password,temp,TWISTERINI, USERHOME, REMOTECONFIGDIRECTORY,
                         PLUGINSDIRECTORY,HTTPSERVERPORT, CENTRALENGINEPORT,
                         RESOURCEALLOCATORPORT, REMOTEDATABASECONFIGPATH,
                         REMOTEDATABASECONFIGFILE, REMOTEEMAILCONFIGPATH,
                         REMOTEEMAILCONFIGFILE,CONFIGDIRECTORY, USERSDIRECTORY,
                         XMLDIRECTORY,  TESTSUITEPATH, LOGSPATH ,XMLREMOTEDIR,REMOTEPLUGINSDIR,
                         REMOTEUSERSDIRECTORY, REMOTEEPIDDIR, REMOTEHARDWARECONFIGDIRECTORY,
                         PLUGINSLOCALGENERALCONF;
    public static Image passicon,testbedicon,porticon,suitaicon, tcicon, propicon,
                        failicon, passwordicon, playicon, stopicon, pauseicon,
                        background,notexecicon,pendingicon,skipicon,stoppedicon,
                        timeouticon,waiticon,workingicon,moduleicon,deviceicon,
                        addsuitaicon,removeicon,vlcclient,vlcserver,switche,
                        flootw,rack150,rack151,rack152,switche2,inicon,outicon,baricon;
    public static boolean run = true;//signal that Twister is not closing
    public static boolean applet; //keeps track if twister is run from applet or localy
    public static IntroScreen intro;    
    private static ArrayList <String []> databaseUserFields = new ArrayList<String[]>();
    public static int LABEL = 0;    
    public static int ID = 1;
    public static int SELECTED = 2;
    public static int MANDATORY = 3;
    public static int ELEMENTSNR = 4;
    private static XmlRpcClient client;
    private static JsonObject inifile;//json structure of conf file saved localy
    private static JsonObject editors, looks;//editors saved by user localy
    private static JsonArray plugins;
    private static String[] lookAndFeels;
    private static Applet container;
    private static Document pluginsconfig;
    
    /*
     * repository initialization method
     * applet - if it is initialized from applet
     * host - server for twister location
     * container - applet or null
     */
    public static void initialize(final boolean applet,String host,Applet container){
        Repository.container = container;
        /*
         * temp folder creation to hold
         * all the needed twister files localy
         */
        try{
            temp = System.getProperty("user.home")+bar+".twister" ;
            File g1 = new File(temp);
            if(g1.mkdir()){
                System.out.println(temp+" succesfuly created");}
            else System.out.println(temp+" could not be created ");
            g1 = new File(temp+bar+host);
            if(g1.mkdir()){
                System.out.println(temp+bar+host+" succesfuly created");}
            else System.out.println(temp+bar+host+" could not be created ");
            temp = g1.getCanonicalPath();}
        catch(Exception e){
            System.out.println("Could not retrieve Temp directory for this OS");
            e.printStackTrace();}
        System.out.println("Temp directory where Twister Directory is created: "+temp);
        File file = new File(Repository.temp+bar+"Twister");
        File twisterhome = new File(System.getProperty("user.home")+bar+".twister");
        /*
         * if file was not deleted on previous
         * Twister exit, delete it now
         */
        if(file.exists()){
            if(Window.deleteTemp(file))
                System.out.println(Repository.temp+bar+"Twister deleted successfull");
            else System.out.println("Could not delete: "+Repository.temp+bar+"Twister");}
        if(!twisterhome.exists()){
            try{if(twisterhome.mkdir())
                    System.out.println(twisterhome.getCanonicalPath()+" succesfuly created");
                else System.out.println("Could not create "+twisterhome.getCanonicalPath());}
            catch(Exception e){
                System.out.println("Could not create "+
                    System.getProperty("user.home")+bar+".twister");
                e.printStackTrace();}}
        /*
         * twiste configuration file
         */
        try{File twisterini = new File(twisterhome.getCanonicalPath()+bar+"twister.conf");
            TWISTERINI = twisterhome.getCanonicalPath()+bar+"twister.conf";
            if(!twisterini.exists()||twisterini.length()==0){// if it does not exist or is empty, create one from scratch 
                if(twisterini.exists())twisterini.delete();
                if(new File(twisterhome.getCanonicalPath()+bar+"twister.conf").createNewFile()){
                    generateJSon();}
                else System.out.println("Could not create twister.conf");}
            parseIni(twisterini);            
        }//parse configuration file
        catch(Exception e){e.printStackTrace();}
        Repository.host = host;
        System.out.println("Setting sftp server to :"+host);
        intro = new IntroScreen();//display intro screen
        intro.setVisible(true);
        intro.setStatus("Started initialization");
        intro.repaint();
        Repository.applet = applet;
        if(applet)System.out.println("Twister running from applet");
        else System.out.println("Twister running from Main");
        try{if(!applet){
                /*
                 * if it did not start from applet
                 * the resources must be loaded from local pc 
                 */
                loadResourcesFromLocal();}
            if(userpassword()){ 
                /*
                 * create directory structure
                 * for twister resources localy
                 */
                System.out.println("Authentication succeeded");
                if(new File(temp+bar+"Twister").mkdir())
                    System.out.println(temp+bar+"Twister"+" folder successfully created");
                else System.out.println("Could not create "+temp+bar+"Twister"+" folder");
                if(new File(temp+bar+"Twister"+bar+"HardwareConfig").mkdir())
                    System.out.println(temp+bar+"Twister"+bar+
                        "HardwareConfig folder successfully created");
                else System.out.println("Could not create "+temp+bar+"Twister"+bar+
                    "HardwareConfig folder");
                if(new File(temp+bar+"Twister"+bar+"XML").mkdir())
                    System.out.println(temp+bar+"Twister"+bar+
                        "XML folder successfully created");
                else System.out.println("Could not create "+temp+bar+"Twister"+
                    bar+"XML folder");
                if(new File(temp+bar+"Twister"+bar+"Users").mkdir()){
                    USERSDIRECTORY = Repository.temp+bar+"Twister"+bar+"Users";
                    System.out.println(temp+bar+"Twister"+bar+
                        "Users folder successfully created");}
                else System.out.println("Could not create "+temp+bar+"Twister"+
                    bar+"Users folder");
                if(new File(temp+bar+"Twister"+bar+"config").mkdir()){
                    CONFIGDIRECTORY = Repository.temp+bar+"Twister"+bar+"config";
                    System.out.println(temp+bar+"Twister"+bar+
                        "config folder successfully created");}
                else System.out.println("Could not create "+temp+bar+
                    "Twister"+bar+"config folder");
                File pluginsdirectory = new File(twisterhome.getCanonicalPath()+
                                                 bar+"Plugins");
                REMOTEPLUGINSDIR = "/opt/twister/plugins";
                if(pluginsdirectory.exists()){
                    PLUGINSDIRECTORY = twisterhome.getCanonicalPath()+bar+"Plugins";
                    System.out.println(twisterhome.getCanonicalPath()+bar+
                                        "Plugins folder found");}
                else if(pluginsdirectory.mkdir()){
                    PLUGINSDIRECTORY = twisterhome.getCanonicalPath()+bar+"Plugins";
                    System.out.println(twisterhome.getCanonicalPath()+
                            bar+"Plugins folder successfully created");}
                else System.out.println("Could not create "+twisterhome.getCanonicalPath()+
                                        bar+"Plugins folder");
                PLUGINSLOCALGENERALCONF = temp+bar+"Twister"+bar+"config"+bar+"plugins.xml";
                intro.setStatus("Started to parse the config");
                intro.addPercent(0.035);
                intro.repaint();
                loadPluginsInterfaces();
                parseConfig();
                if(!getPluginsFile())createGeneralPluginConf();
                if(!parsePluginsConfig(CONFIGDIRECTORY+"/plugins.xml")){
                    System.out.println("There was a problem in parsing"+
                                       " plugins configuration");}
                                       
                /*
                 * XmlRpc main connection used by Twister framework
                 */
                try{XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
                    configuration.setServerURL(new URL("http://"+Repository.host+
                                                ":"+Repository.getCentralEnginePort()));
                    client = new XmlRpcClient();
                    client.setConfig(configuration);
                    System.out.println("Client initialized: "+client);}
                catch(Exception e){System.out.println("Could not conect to "+
                                    Repository.host+" :"+Repository.getCentralEnginePort()+
                                    "for RPC client initialization");}
                intro.setStatus("Finished parsing the config");
                intro.addPercent(0.035);
                intro.repaint();
                parseDBConfig(Repository.REMOTEDATABASECONFIGFILE,true);
                window = new Window(applet,container);
                parseEmailConfig(Repository.REMOTEEMAILCONFIGFILE,true);
                variables.put("user",user);
                variables.put("password",password);  
                variables.put("temp",temp);
                variables.put("inifile",TWISTERINI);
                variables.put("remoteuserhome",USERHOME);  
                variables.put("remotconfigdir",REMOTECONFIGDIRECTORY);  
                variables.put("localplugindir",PLUGINSDIRECTORY);  
                variables.put("httpserverport",HTTPSERVERPORT);  
                variables.put("centralengineport",CENTRALENGINEPORT);  
                variables.put("resourceallocatorport",RESOURCEALLOCATORPORT);  
                variables.put("remotedatabaseparth",REMOTEDATABASECONFIGPATH);
                variables.put("remotedatabasefile",REMOTEDATABASECONFIGFILE);
                variables.put("remoteemailpath",REMOTEEMAILCONFIGPATH);
                variables.put("remoteemailfile",REMOTEEMAILCONFIGFILE);
                variables.put("configdir",CONFIGDIRECTORY);
                variables.put("usersdir",USERSDIRECTORY);
                variables.put("masterxmldir",XMLDIRECTORY);
                variables.put("testsuitepath",TESTSUITEPATH);
                variables.put("logspath",LOGSPATH);
                variables.put("masterxmlremotedir",XMLREMOTEDIR);
                variables.put("remotehwconfdir",REMOTEHARDWARECONFIGDIRECTORY);
                variables.put("remoteepdir",REMOTEEPIDDIR);
                variables.put("remoteusersdir",REMOTEUSERSDIRECTORY);
                variables.put("pluginslocalgeneralconf",PLUGINSLOCALGENERALCONF);
                variables.put("remotegeneralpluginsdir",REMOTEPLUGINSDIR);
            }
            else{
                /*
                 * if login is not scucces remove temp folder
                 * and exit application
                 */
                if(Window.deleteTemp(file))
                    System.out.println(Repository.temp+bar+"Twister deleted successfull");
                else System.out.println("Could not delete: "+temp+bar+"Twister");
                intro.dispose();
                run = false;
                if(!applet)System.exit(0);}}
        catch(Exception e){e.printStackTrace();}}
        
    /*
     * method to create general plugin
     * configuration file 
     */
    public static void createGeneralPluginConf(){
        try{
            DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
            Document document = documentBuilder.newDocument();
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            DOMSource source = new DOMSource(document);
            Element rootElement = document.createElement("Root");
            document.appendChild(rootElement);
            File file = new File(Repository.PLUGINSLOCALGENERALCONF);
            Result result = new StreamResult(file);
            transformer.transform(source, result);
            Repository.c.cd(Repository.USERHOME+"/twister/config/");
            System.out.println("Saving to: "+Repository.USERHOME+"/twister/config/");
            FileInputStream in = new FileInputStream(file);
            Repository.c.put(in, file.getName());
            in.close();}
        catch(Exception e){
            System.out.println("There was a problem in generating Plugins general config");
            e.printStackTrace();
        }
    }
      
    /*
     * method to load plugininterfaces
     * to be available on initializing Plugins
     */
    public static void loadPluginsInterfaces(){
        Plugins.deletePlugins();
        Plugins.copyPlugin("Twister.jar");
        Plugins.copyPlugin("xmlrpc-client-3.1.3.jar");
        Plugins.copyPlugin("xmlrpc-common-3.1.3.jar");
        PluginsLoader.setClassPath();
    }
        
    /*
     * load resources needed for framework
     * from local pc
     */
    public static void loadResourcesFromLocal()throws Exception{
        InputStream in;
        in = Repository.class.getResourceAsStream("Icons"+bar+"background.png"); 
        background = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"vlcclient.png"); 
        vlcclient = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"vlcserver.png"); 
        vlcserver = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"switch.png"); 
        switche = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"twisterfloodlight.png"); 
        flootw = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"150.png"); 
        rack150 = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"151.png"); 
        rack151 = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"152.png"); 
        rack152 = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"switch.jpg"); 
        switche2 = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"in.png"); 
        inicon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"out.png"); 
        outicon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"bar.png"); 
        baricon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"port.png"); 
        porticon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"deleteicon.png");
        removeicon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"addsuita.png"); 
        addsuitaicon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"device.png"); 
        deviceicon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"module.png"); 
        moduleicon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"tc.png"); 
        tcicon = new ImageIcon(ImageIO.read(in)).getImage(); 
        in = Repository.class.getResourceAsStream("Icons"+bar+"suita.png"); 
        suitaicon = new ImageIcon(ImageIO.read(in)).getImage(); 
        in = Repository.class.getResourceAsStream("Icons"+bar+"prop.png"); 
        propicon = new ImageIcon(ImageIO.read(in)).getImage(); 
        in = Repository.class.getResourceAsStream("Icons"+bar+"fail.png"); 
        failicon = new ImageIcon(ImageIO.read(in)).getImage(); 
        in = Repository.class.getResourceAsStream("Icons"+bar+"pass.png");
        passicon = new ImageIcon(ImageIO.read(in)).getImage(); 
        in = Repository.class.getResourceAsStream("Icons"+bar+"stop.png");
        stopicon = new ImageIcon(ImageIO.read(in)).getImage(); 
        in = Repository.class.getResourceAsStream("Icons"+bar+"play.png");
        playicon = new ImageIcon(ImageIO.read(in)).getImage();                 
        in = Repository.class.getResourceAsStream("Icons"+bar+"notexec.png");
        notexecicon = new ImageIcon(ImageIO.read(in)).getImage(); 
        in = Repository.class.getResourceAsStream("Icons"+bar+"pending.png");
        pendingicon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"skip.png");
        skipicon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"stopped.png");
        stoppedicon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"timeout.png");
        timeouticon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"waiting.png");
        waiticon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"passwordicon.png");
        passwordicon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"working.png");
        workingicon = new ImageIcon(ImageIO.read(in)).getImage();                
        in = Repository.class.getResourceAsStream("Icons"+bar+"pause.png");
        pauseicon = new ImageIcon(ImageIO.read(in)).getImage();
        in = Repository.class.getResourceAsStream("Icons"+bar+"testbed.png");
        testbedicon = new ImageIcon(ImageIO.read(in)).getImage();
        in.close();}
        
    /*
     * generate local config 
     * file from scratch
     */
    public static void generateJSon(){
        JsonObject root = new JsonObject();
        JsonObject array =new JsonObject();
        array.addProperty("Embedded", "embedded");
        array.addProperty("DEFAULT", "Embedded");
        JsonObject array2 =new JsonObject();
        array2.addProperty("NimbusLookAndFeel", "javax.swing.plaf.nimbus.NimbusLookAndFeel");
        array2.addProperty("MetalLookAndFeel", "javax.swing.plaf.metal.MetalLookAndFeel");
        array2.addProperty("MotifLookAndFeel", "com.sun.java.swing.plaf.motif.MotifLookAndFeel");
        array2.addProperty("WindowsLookAndFeel", "com.sun.java.swing.plaf.windows.WindowsLookAndFeel");
        array2.addProperty("JGoodiesWindowsLookAndFeel", "com.jgoodies.looks.windows.WindowsLookAndFeel");
        array2.addProperty("Plastic3DLookAndFeel", "com.jgoodies.looks.plastic.Plastic3DLookAndFeel");
        array2.addProperty("PlasticXPLookAndFeel", "com.jgoodies.looks.plastic.PlasticXPLookAndFeel");
        array2.addProperty("DEFAULT", "MetalLookAndFeel");
        root.add("plugins", new JsonArray());
        root.add("editors", array);
        root.add("looks", array2);
        try{FileWriter writer = new FileWriter(TWISTERINI);
            Gson gson = new GsonBuilder().setPrettyPrinting().create(); 
            writer.write(gson.toJson(root));
            writer.close();}
        catch(Exception e){
            System.out.println("Could not write default JSon to twister.conf");
            e.printStackTrace();}
        System.out.println("twister.conf succesfuly created");}
    
    /*
     * set UI Look based on
     * user selection
     */
    public static void setUILook(final String look){
        SwingUtilities.invokeLater(new Runnable(){
            public void run(){
                System.out.println("Setting UI: "+look);
                try{UIManager.setLookAndFeel(Repository.getLooks().get(look).getAsString());
                    if(applet){SwingUtilities.updateComponentTreeUI(container);}
                    else if(window!=null){SwingUtilities.updateComponentTreeUI(window);}}
                catch(Exception e){e.printStackTrace();}}});}
        
    /*
     * attempt to connect with sftp to server
     */ 
    public static boolean userpassword(){
        boolean passed = false;
        while(!passed){
            try{JTextField user1 = new JTextField();   
                JPasswordField password1 = new JPasswordField();
                JComboBox combo = new JComboBox();
                try{populateLookAndFeels();
                    if(lookAndFeels!=null){
                        int index = populateCombo(combo,lookAndFeels);
                        if(index>-1)combo.setSelectedIndex(index);}}
                catch(Exception e){
                    System.out.println("Error in setting LookAndFeel");
                    e.printStackTrace();}
                JPanel p = getPasswordPanel(user1,password1,combo);
                int resp = (Integer)CustomDialog.showDialog(p,JOptionPane.QUESTION_MESSAGE,
                                                            JOptionPane.OK_CANCEL_OPTION, 
                                                            null, "User & Password",
                                                            new ImageIcon(Repository.getPasswordIcon()));
                if(resp == JOptionPane.OK_OPTION){
                    System.out.println("Attempting to connect to: "+host+
                        " with user: "+user1.getText()+" and password: "+
                        password1.getPassword());
                    JSch jsch = new JSch();
                    user = user1.getText();
                    Session session = jsch.getSession(user, host, 22);
                    Repository.password = new String(password1.getPassword());
                    session.setPassword(new String(password1.getPassword()));
                    Properties config = new Properties();
                    config.put("StrictHostKeyChecking", "no");
                    session.setConfig(config);
                    session.connect();
                    Channel channel = session.openChannel("sftp");
                    channel.connect();
                    c = (ChannelSftp)channel;
                    try{USERHOME = c.pwd();}
                    catch(Exception e){
                        System.out.println("ERROR: Could not retrieve remote user home directory");}
                    REMOTECONFIGDIRECTORY = USERHOME+"/twister/config/";
                    passed = true;
                    if(combo.getItemCount()>0)setUILook(combo.getSelectedItem().toString());}
                else return false;}
            catch(JSchException ex){
                if(ex.toString().indexOf("Auth fail")!=-1)
                    System.out.println("wrong user and/or password");
                else{ex.printStackTrace();
                    System.out.println("Could not connect to server");}}}
        return true;}        
      
    /*
     * method used to reset database config
     */
    public static void resetDBConf(String filename,boolean server){
        databaseUserFields.clear();
        System.out.println("Reparsing "+filename);
        parseDBConfig(filename,server);
        window.mainpanel.p1.suitaDetails.restart(databaseUserFields);}
        
    /*
     * method used to reset Email config
     */
    public static void resetEmailConf(String filename,boolean server){
        System.out.println("Reparsing "+filename);
        parseEmailConfig(filename,server);}
        
    /*
     * method to get database config file
     * name - file name
     * fromserver - if from server(true) else from local temp folder
     */
    public static File getDBConfFile(String name,boolean fromServer){
        File file = new File(temp+bar+"Twister"+bar+"config"+bar+name);
        if(fromServer){
            InputStream in = null;
            try{c.cd(Repository.REMOTEDATABASECONFIGPATH);}
            catch(Exception e){
                System.out.println("Could not get :"+Repository.REMOTEDATABASECONFIGPATH);}
            System.out.print("Getting "+name+" as database config file.... ");
            try{in = c.get(name);
                InputStreamReader inputStreamReader = new InputStreamReader(in);
                BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
                BufferedWriter writer = null;
                String line;
                try{writer = new BufferedWriter(new FileWriter(file));
                    while ((line=bufferedReader.readLine())!= null){
                        writer.write(line);
                        writer.newLine();}
                    bufferedReader.close();
                    writer.close();
                    inputStreamReader.close();
                    in.close();
                    System.out.println("successfull");}
                catch(Exception e){
                    System.out.println("failed");
                    e.printStackTrace();}}
            catch(Exception e){
                System.out.println("Could not get :"+
                    name+" from: "+Repository.REMOTEDATABASECONFIGPATH+
                    " as database config file");}}
        return file;}
        
        
    /*
     * method to get Email config file
     * name - file name
     * fromserver - if from server(true) else from local temp folder
     */    
    public static File getEmailConfFile(String name,boolean fromServer){
        File file = new File(temp+bar+"Twister"+bar+"config"+bar+name);
        if(fromServer){
            InputStream in = null;
            try{c.cd(Repository.REMOTEEMAILCONFIGPATH);}
            catch(Exception e){
                System.out.println("Could not get :"+Repository.REMOTEEMAILCONFIGPATH);}
            System.out.print("Getting "+name+" as email config file.... ");
            try{in = c.get(name);
                InputStreamReader inputStreamReader = new InputStreamReader(in);
                BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
                BufferedWriter writer = null;
                String line;
                try{writer = new BufferedWriter(new FileWriter(file));
                    while ((line=bufferedReader.readLine())!= null){
                        writer.write(line);
                        writer.newLine();}
                    bufferedReader.close();
                    writer.close();
                    inputStreamReader.close();
                    in.close();
                    System.out.println("successfull");}
                catch(Exception e){
                    System.out.println("failed");
                    e.printStackTrace();}}
            catch(Exception e){
                System.out.println("Could not get :"+name+
                " from: "+Repository.REMOTEEMAILCONFIGPATH+" as email config file");}}
        return file;}
     
    /*
     * parse database config file
     * name - file name
     * fromserver - true - false
     */
    public static DefaultMutableTreeNode parseDBConfig(String name,boolean fromServer){
        File dbConf = getDBConfFile(name,fromServer);
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DefaultMutableTreeNode root = new DefaultMutableTreeNode("Root");
        try{DocumentBuilder db = dbf.newDocumentBuilder();
            Document doc = db.parse(dbConf);
            doc.getDocumentElement().normalize();                
            NodeList nodeLst = doc.getElementsByTagName("table_structure");      
            for(int i=0;i<nodeLst.getLength();i++){
                Element tablee = (Element)nodeLst.item(i);
                NodeList fields = tablee.getElementsByTagName("field");
                DefaultMutableTreeNode table = new DefaultMutableTreeNode(tablee.getAttribute("name"));
                for(int j=0;j<fields.getLength();j++){
                    Element fielde = (Element)fields.item(j);   
                    DefaultMutableTreeNode field = new DefaultMutableTreeNode(fielde.getAttribute("Field"));
                    table.add(field);}
                root.add(table);}
            nodeLst = doc.getElementsByTagName("twister_user_defined");
            Element tablee = (Element)nodeLst.item(0);
            NodeList fields = tablee.getElementsByTagName("field_section");
            tablee = (Element)fields.item(0);
            fields = tablee.getElementsByTagName("field");
            for(int i=0;i<fields.getLength();i++){                
                tablee = (Element)fields.item(i);
                if(tablee.getAttribute("GUIDefined").equals("true")){
                    String field [] = new String[ELEMENTSNR];
                    field[0]=tablee.getAttribute("Label");
                    if(field[0]==null){
                        System.out.println("Warning, no Label element in"+
                                            " field tag in db.xml at filed nr: "+i);
                        field[0]="";}
                    field[1]=tablee.getAttribute("ID");
                    if(field[1]==null){
                        System.out.println("Warning, no ID element in "+
                                            "field tag in db.xml at filed nr: "+i);
                        field[1]="";}
                    field[2]=tablee.getAttribute("Type");
                    if(field[2]==null){
                        System.out.println("Warning, no Type element in"+
                                            " field tag in db.xml at filed nr: "+i);
                        field[2]="";}
                    field[3]=tablee.getAttribute("Mandatory");
                    if(field[3]==null){
                        System.out.println("Warning, no Mandatory element "+
                                            "in field tag in db.xml at filed nr: "+i);
                        field[3]="";}
                    databaseUserFields.add(field);}}}
        catch(Exception e){
            try{System.out.println("Could not parse batabase XML file: "+dbConf.getCanonicalPath());}
            catch(Exception ex){
                System.out.println("There is a problem with "+name+" file");
                ex.printStackTrace();}
            e.printStackTrace();}
        return root;}
        
    /*
     * parse email config file
     */
    public static void parseEmailConfig(String name,boolean fromServer){
        File dbConf = getEmailConfFile(name,fromServer);
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        try{DocumentBuilder db = dbf.newDocumentBuilder();
            Document doc = db.parse(dbConf);
            doc.getDocumentElement().normalize();                
            window.mainpanel.p4.getEmails().setCheck(Boolean.parseBoolean(getTagContent(doc, "Enabled")));
            String smtppath = getTagContent(doc, "SMTPPath");
            window.mainpanel.p4.getEmails().setIPName(smtppath.split(":")[0]);
            window.mainpanel.p4.getEmails().setPort(smtppath.split(":")[1]);
            window.mainpanel.p4.getEmails().setUser(getTagContent(doc, "SMTPUser"));
            window.mainpanel.p4.getEmails().setFrom(getTagContent(doc, "From"));
            window.mainpanel.p4.getEmails().setEmails(getTagContent(doc, "To"));
            if(!getTagContent(doc, "SMTPPwd").equals("")){
                window.mainpanel.p4.getEmails().setPassword("****");}
            window.mainpanel.p4.getEmails().setMessage(getTagContent(doc, "Message"));
            window.mainpanel.p4.getEmails().setSubject(getTagContent(doc, "Subject"));}
        catch(Exception e){e.printStackTrace();}}
        
        
    /*
     * parse main fwmconfig file
     */
    public static void parseConfig(){ 
        try{InputStream in = null;
            byte[] data = new byte[100]; 
            int nRead;
            ByteArrayOutputStream buffer = new ByteArrayOutputStream();
            OutputStream out=null;
            InputStreamReader inputStreamReader = null;
            BufferedReader bufferedReader = null;  
            BufferedWriter writer=null;
            File file;
            String line = null;
            String name = null;
            try{c.cd(USERHOME+"/twister/config/");}
            catch(Exception e){
                System.out.println("Could not get :"+USERHOME+"/twister/config/");
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,Repository.window,
                                        "Warning", "Could not get :"+USERHOME+
                                        "/twister/config/");
                if(Window.deleteTemp(new File(Repository.temp+bar+"Twister")))
                    System.out.println(Repository.temp+bar+"Twister deleted successfull");
                else System.out.println("Could not delete: "+Repository.temp+bar+"Twister");
                run = false;
                if(!applet)System.exit(0);}
            try{System.out.println("fwmconfig.xml size on sftp: "+
                        c.lstat("fwmconfig.xml").getSize()+" bytes");
                in = c.get("fwmconfig.xml");}
            catch(Exception e){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Repository.window,
                                        "Warning","Could not get fwmconfig.xml from "+
                                        c.pwd()+" creating a blank one.");
                System.out.println("Could not get fwmconfig.xml from "+
                                        c.pwd()+" creating a blank one.");
                ConfigFiles.saveXML(true);
                in = c.get("fwmconfig.xml");}
            inputStreamReader = new InputStreamReader(in);
            bufferedReader = new BufferedReader(inputStreamReader);  
            file = new File(temp+bar+"Twister"+bar+"config"+bar+"fwmconfig.xml");
            writer = new BufferedWriter(new FileWriter(file));
            while((line=bufferedReader.readLine())!= null){
                writer.write(line);
                writer.newLine();}
            bufferedReader.close();
            writer.close();
            inputStreamReader.close();
            in.close();
            System.out.println("fwmconfig.xml local size: "+file.length()+" bytes");
            String usersdir="";
            intro.setStatus("Finished getting fwmconfig");
            intro.addPercent(0.035);
            intro.repaint();
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            try{DocumentBuilder db = dbf.newDocumentBuilder();
                Document doc = db.parse(Repository.getFwmConfig());
                doc.getDocumentElement().normalize();    
                LOGSPATH = getTagContent(doc,"LogsPath");
                if(doc.getElementsByTagName("LogFiles").getLength()==0)
                    System.out.println("LogFiles tag not found in fwmconfig");
                else{logs.add(getTagContent(doc,"logRunning"));
                    logs.add(getTagContent(doc,"logDebug"));
                    logs.add(getTagContent(doc,"logSummary"));
                    logs.add(getTagContent(doc,"logTest"));
                    logs.add(getTagContent(doc,"logCli"));}
                HTTPSERVERPORT = getTagContent(doc,"HttpServerPort");
                CENTRALENGINEPORT = getTagContent(doc,"CentralEnginePort");
                RESOURCEALLOCATORPORT = getTagContent(doc,"ResourceAllocatorPort");
                usersdir = getTagContent(doc,"UsersPath");
                REMOTEUSERSDIRECTORY = usersdir;
                XMLREMOTEDIR = getTagContent(doc,"MasterXMLTestSuite");
                XMLDIRECTORY = Repository.temp+bar+"Twister"+bar+"XML"+
                                        bar+XMLREMOTEDIR.split("/")[XMLREMOTEDIR.split("/").length-1];
                REMOTEEPIDDIR = getTagContent(doc,"EPIdsFile");
                REMOTEDATABASECONFIGFILE = getTagContent(doc,"DbConfigFile");
                String [] path = REMOTEDATABASECONFIGFILE.split("/");
                StringBuffer result = new StringBuffer();
                if (path.length > 0) {
                    for (int i=0; i<path.length-1; i++){
                        result.append(path[i]);
                        result.append("/");}}
                REMOTEDATABASECONFIGPATH = result.toString();
                REMOTEDATABASECONFIGFILE = path[path.length-1];
                REMOTEEMAILCONFIGFILE = getTagContent(doc,"EmailConfigFile");
                path = REMOTEEMAILCONFIGFILE.split("/");
                result = new StringBuffer();
                if (path.length > 0) {
                    for (int i=0; i<path.length-1; i++){
                        result.append(path[i]);
                        result.append("/");}}
                REMOTEEMAILCONFIGPATH = result.toString();
                REMOTEEMAILCONFIGFILE = path[path.length-1];
                TESTSUITEPATH = getTagContent(doc,"TestCaseSourcePath");
                REMOTEHARDWARECONFIGDIRECTORY = getTagContent(doc,"HardwareConfig");}
            catch(Exception e){e.printStackTrace();}
            intro.setStatus("Finished initializing variables fwmconfig");
            intro.addPercent(0.035);
            intro.repaint();
            intro.setStatus("Started getting users xml");
            intro.addPercent(0.035);
            intro.repaint();
            try{c.cd(usersdir);}
            catch(Exception e){
                System.out.println("Could not get to "+usersdir+"on sftp");}
            int subdirnr = usersdir.split("/").length-1;
            int size ;
            try{size= c.ls(usersdir).size();}
            catch(Exception e){
                System.out.println("No suites xml");
                size=0;}
            for(int i=0;i<size;i++){
                name = ((LsEntry)c.ls(usersdir).get(i)).getFilename();
                if(name.split("\\.").length==0)continue; 
                if(name.toLowerCase().indexOf(".xml")==-1)continue;
                System.out.print("Getting "+name+" ....");
                in = c.get(name);
                inputStreamReader = new InputStreamReader(in);
                bufferedReader = new BufferedReader(inputStreamReader);
                file = new File(temp+bar+"Twister"+bar+"Users"+bar+name);
                writer = new BufferedWriter(new FileWriter(file));
                while ((line=bufferedReader.readLine())!= null){
                    writer.write(line);
                    writer.newLine();}
                bufferedReader.close();
                writer.close();
                inputStreamReader.close();
                in.close();
                System.out.println("successfull");}
            intro.setStatus("Finished getting users xml");
            intro.addPercent(0.035);
            intro.repaint();
            String dir = Repository.getXMLRemoteDir();
            String [] path = dir.split("/");
            StringBuffer result = new StringBuffer();
            if (path.length > 0) {
                for (int i=0; i<path.length-2; i++){
                    result.append(path[i]);
                    result.append("/");}}
            intro.setStatus("Finished writing xml path");
            intro.addPercent(0.035);
            intro.repaint();
            int length = 0;
            try{length = c.ls(result.toString()+path[path.length-2]).size();}
            catch(Exception e){
                System.out.println("Could not get "+result.toString()+dir);}
            if(length>2){
                intro.setStatus("Started looking for xml file");
                intro.addPercent(0.035);
                intro.repaint();
                intro.setStatus("Started getting xml file");
                intro.addPercent(0.035);
                intro.repaint();
                System.out.println("XMLREMOTEDIR: "+XMLREMOTEDIR);
                in = c.get(XMLREMOTEDIR);                
                data = new byte[900];
                buffer = new ByteArrayOutputStream();
                while ((nRead = in.read(data, 0, data.length)) != -1){
                    buffer.write(data, 0, nRead);}
                intro.setStatus("Finished reading xml ");
                intro.addPercent(0.035);
                intro.repaint();
                buffer.flush();
                out = new FileOutputStream(temp+bar+"Twister"+bar+"XML"+
                            bar+XMLREMOTEDIR.split("/")[XMLREMOTEDIR.split("/").length-1]);
                intro.setStatus("Started writing xml file");
                intro.addPercent(0.035);
                intro.repaint();
                buffer.writeTo(out);
                out.close();
                buffer.close();
                in.close();}
            intro.setStatus("Finished writing xml");
            intro.addPercent(0.035);
            intro.repaint();}
        catch(Exception e){e.printStackTrace();}}
        
    /*
     * method to get tag content from xml
     * doc - xml document
     * tag - tag name
     */
    public static String getTagContent(Document doc, String tag){
        NodeList nodeLst = doc.getElementsByTagName(tag);
        if(nodeLst.getLength()==0)
            System.out.println("tag "+tag+" not found in "+doc.getDocumentURI());
        Node fstNode = nodeLst.item(0);
        Element fstElmnt = (Element)fstNode;
        NodeList fstNm = fstElmnt.getChildNodes();
        String temp;
        try{temp = fstNm.item(0).getNodeValue().toString();}
        catch(Exception e){
            System.out.println(tag+" empty");
            temp = "";}
        return temp;}
        
    /*
     * parser for conf twister file
     */
    public static void parseIni(File ini){
        try{FileInputStream in  = new FileInputStream(ini);
            InputStreamReader inputStreamReader = new InputStreamReader(in);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);  
            StringBuffer b=new StringBuffer("");
            String line;
            try{while ((line=bufferedReader.readLine())!= null){b.append(line);}
                bufferedReader.close();
                inputStreamReader.close();
                in.close();}
            catch(Exception e){e.printStackTrace();}
            line = b.toString();
            JsonElement jelement = new JsonParser().parse(line);
            inifile = jelement.getAsJsonObject();
            editors = inifile.getAsJsonObject("editors");
            looks = inifile.getAsJsonObject("looks");
            plugins = inifile.getAsJsonArray("plugins");
            if(plugins==null){
                inifile.add("plugins", new JsonArray());
                writeJSon();
                plugins = inifile.getAsJsonArray("plugins");}
            System.out.println("Editors: "+editors.toString());}
        catch(Exception e){
            System.out.print("Could not parse ini file: ");
            try{System.out.println(ini.getCanonicalPath());}
            catch(Exception ex){ex.printStackTrace();}
            e.printStackTrace();}}
            
    /*
     * method to add suite to suite list
     */
    public static void addSuita(Item s){
        suite.add(s);}
        
    /*
     * method to get suite from suite list
     * s - suite index in list
     */
    public static Item getSuita(int s){
        return suite.get(s);}
        
    /*
     * method to get suite list size
     */ 
    public static int getSuiteNr(){
        return suite.size();}
            
    /*
     * method to get Database User Fields
     * set from twister
     */ 
    public static ArrayList<String[]> getDatabaseUserFields(){
        return databaseUserFields;}
      
    /*
     * clear all suite from test suite list
     */
    public static void emptyTestRepository(){
        suitetest.clear();}        
        
    /*
     * clear the list of logs tracked by Twister
     */
    public static void emptyLogs(){
        logs.clear();}    
         
    /*
     * method to get config file from local pc
     */
    public static File getFwmConfig(){
        return new File(temp+bar+"Twister"+bar+"config"+bar+"fwmconfig.xml");}
    /*
     * users directory from temp folder on local pc
     */  
    public static String getUsersDirectory(){
        return USERSDIRECTORY;}
        
    /*
     * Ep directory from server
     */ 
    public static String getRemoteEpIdDir(){
        return REMOTEEPIDDIR;}        
        
    /*
     * Users directory from server
     */ 
    public static String getRemoteUsersDirectory(){
        return REMOTEUSERSDIRECTORY;}
        
    /*
     * CentralEnginePort set by fwmconfig file
     */ 
    public static String getCentralEnginePort(){
        return CENTRALENGINEPORT;}
        
    /*
     * ResourceAllocatorPort set by fwmconfig file
     */ 
    public static String getResourceAllocatorPort(){
        return RESOURCEALLOCATORPORT;}
        
    /*
     * test suite xml directory from server
     */ 
    public static String getXMLRemoteDir(){
        return XMLREMOTEDIR;}
    
    /*
     * suite list from repository
     */
    public static ArrayList<Item> getSuite(){
        return suite;}
        
    /*
     * test suite list from repository
     */
    public static ArrayList<Item> getTestSuite(){
        return suitetest;}
    
    /*
     * test suite list size from repository
     */
    public static int getTestSuiteNr(){
        return suitetest.size();}

    /*
     * local config directory from temp
     */
    public static String getConfigDirectory(){
        return CONFIGDIRECTORY;}
        
    /*
     * add suite to test suite list
     */
    public static void addTestSuita(Item suita){
        suitetest.add(suita);}
    
    /*
     * HTTPServerPort set by fwmconfig file
     */
    public static String getHTTPServerPort(){
        return HTTPSERVERPORT;}
        
    /*
     * method to get suite from test suite list 
     * i - suite index in test suite list
     */
    public static Item getTestSuita(int i){
        return suitetest.get(i);}
    
    /*
     * test suite path on server
     */
    public static String getTestSuitePath(){
        return TESTSUITEPATH;}

    /*
     * empty suites list in Repository
     */
    public static void emptySuites(){
        suite.clear();}
        
    /*
     * test suite xml local directory
     */
    public static String getTestXMLDirectory(){
        return XMLDIRECTORY;}
        
     /*
      * declare posible looksAndFeel
      */
    private static void populateLookAndFeels(){
        JsonObject looks = Repository.getLooks();
        if(looks!=null){
            int length = looks.entrySet().size();
            Iterator iter = looks.entrySet().iterator();
            Entry entry;
            String [] vecresult;
            if(looks.get("DEFAULT")!=null)lookAndFeels = new String[length-1];
            else lookAndFeels = new String[length];
            int index = 0;
            for(int i=0;i<length;i++){                        
                entry = (Entry)iter.next();
                if(entry.getKey().toString().equals("DEFAULT"))continue;
                lookAndFeels[index] = (String)entry.getKey();
                index++;}}
        else{System.out.println("Error: No LooksAndFeels set, using default look");}}
        
     /*
      *populate lookandfeel cobo
      *with looks and feels that are
      *available
      */
    private static int populateCombo(JComboBox combo,String[]list){
        int index = -1;
        String name;
        for(int i=0;i<list.length;i++){
            try{Class.forName(getLooks().get(list[i]).getAsString());                
                combo.addItem(list[i]);
                if(Repository.getDefaultLook().equals(list[i])){
                    index = i;}}
            catch(Exception e){continue;}}
        return index;}
        
    /*
     * panel displayed on
     * twister startup for user and password
     * input
     */    
    public static JPanel getPasswordPanel(JTextField jTextField1,
                JPasswordField jTextField2,final JComboBox combo){
        final JCheckBox check = new JCheckBox("Default");
        check.setSelected(true);
        JPanel p = new JPanel();
        p.setLayout(new BoxLayout(p, BoxLayout.Y_AXIS));
        JPanel jPanel1 = new JPanel();
        JLabel jLabel3 = new JLabel();
        JPanel jPanel2 = new JPanel();
        JLabel jLabel4 = new JLabel();
        JPanel jPanel5 = new JPanel();
        jPanel5.add(combo);
        jPanel5.add(check);
        jPanel1.setLayout(new java.awt.BorderLayout());
        jLabel3.setText("User: ");
        jPanel1.add(jLabel3, BorderLayout.CENTER);
        p.add(jPanel1);
        p.add(jTextField1);
        jPanel2.setLayout(new BorderLayout());
        jLabel4.setText("Password: ");
        jPanel2.add(jLabel4, BorderLayout.CENTER);
        p.add(jPanel2);
        p.add(jTextField2);
        p.add(jPanel5);
        combo.addItemListener(new ItemListener(){
            public void itemStateChanged(ItemEvent evt){
                if(evt.getStateChange() == ItemEvent.SELECTED){
                    if(Repository.getDefaultLook().equals(evt.getItem().toString()))
                        check.setSelected(true);
                    else check.setSelected(false);}}});
        check.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(getLooks()!=null){
                    if(check.isSelected())
                        Repository.setDefaultLook(combo.getSelectedItem().toString());
                    else Repository.setDefaultLook("MetalLookAndFeel");}}});
        return p;}
        
    /*
     * Twister icons
     */    
    public static Image getSuitaIcon(){
        return suitaicon;}
    
    public static Image getFailIcon(){
        return failicon;}
        
    public static Image getPendingIcon(){
        return pendingicon;}
        
    public static Image getWorkingIcon(){
        return workingicon;}
        
    public static Image getNotExecIcon(){
        return notexecicon;}
        
    public static Image getTimeoutIcon(){
        return timeouticon;}
        
    public static Image getSkippedIcon(){
        return skipicon;}
        
    public static Image getWaitingIcon(){
        return waiticon;}
        
    public static Image getStopIcon(){
        return stopicon;}
        
    public static Image getTestBedIcon(){
        return testbedicon;}
        
     public static Image getStoppedIcon(){
        return stoppedicon;}
        
    public static Image getPassIcon(){
        return passicon;}
        
    public static Image getTCIcon(){
        return tcicon;}
        
    public static Image getPlayIcon(){
        return playicon;}
        
    public static String getBar(){
        return bar;}
        
    public static Image getPropertyIcon(){
        return propicon;}
        
    public static Image getPasswordIcon(){
        return passwordicon;}
        
    /*
     * looks saved in conf file
     */
    public static JsonObject getLooks(){
        return looks;}
        
    /*
     * plugins saved in conf file
     */
    public static JsonArray getPlugins(){
        return plugins;}
        
    /*
     * default look name
     * saved in json list
     * 
     */ 
    public static String getDefaultLook(){
        return getLooks().get("DEFAULT").getAsJsonPrimitive().getAsString();}
        
    /*
     * write default look
     * in json list and in local conf     * 
     */
    public static void setDefaultLook(String look){
        addLook(new String[]{"DEFAULT",look});
        writeJSon();}
        
    /*
     * add user defined look to list
     * of looks
     */
    public static void addLook(String [] look){
        getLooks().add(look[0],new JsonPrimitive(look[1]));
        writeJSon();}
        
        
    /*
     * method to remove plugin
     * from inifile based on filename of plugin
     */
    public static void removePlugin(String filename){
        JsonArray array = new JsonArray();
        int size = getPlugins().size();
        for(int i=0;i<size;i++){
            if(getPlugins().get(i).getAsString().equals(filename))continue;
            array.add(getPlugins().get(i));}
        plugins = array;
        inifile.add("plugins", array);
        writeJSon();}
        
    /*
     * editors saved in conf file
     */
    public static JsonObject getEditors(){
        return editors;}
      
    /*
     * delete editor from editors list
     * and save file
     */        
    public static void removeEditor(String editor){
        editors.remove(editor);
        writeJSon();}
        
    /*
     * add user defined editor to list
     * of editors
     */
    public static void addEditor(String [] editor){
        getEditors().add(editor[0],new JsonPrimitive(editor[1]));
        writeJSon();}
        
    /*
     * add plugin to list
     * of plugins
     */
    public static void addPlugin(String pluginfilename){
        if(getPlugins().isJsonArray()){
            getPlugins().getAsJsonArray().add(new JsonPrimitive(pluginfilename));}
        else{JsonPrimitive primitive = new JsonPrimitive(pluginfilename);
            JsonArray array = new JsonArray();
            array.add(primitive);
            inifile.add("plugins",array);}
        writeJSon();}
    /*
     * default editor name
     * saved in json list
     * 
     */ 
    public static String getDefaultEditor(){
        return getEditors().get("DEFAULT").getAsJsonPrimitive().getAsString();}
        
    /*
     * write default editor
     * in json list and in local conf     * 
     */
    public static void setDefaultEditor(String editor){
        addEditor(new String[]{"DEFAULT",editor});
        writeJSon();}
        
    /*
     * write local conf 
     * with saved json
     */
    public static void writeJSon(){        
        try{Writer writer = new OutputStreamWriter(new FileOutputStream(TWISTERINI));
            Gson gson = new GsonBuilder().setPrettyPrinting().create(); 
            gson.toJson(inifile, writer);
            writer.close();}
        catch(Exception e){
            System.out.println("Could not write to local config file");
            e.printStackTrace();}}
    
    /*
     * logs tracked by twister framwork
     */
    public static ArrayList<String> getLogs(){
        return logs;}
        
    /*
     * RPC connection
     */
    public static XmlRpcClient getRPCClient(){
        return client;}

    /*
     * user used on twister server
     */
    public static String getUser(){
        return user;}
    
    /*
     * variables as hashtable used
     * by plugins
     */
    public static Hashtable getVariables(){
        return variables;}
    
    /*
     * method to get pluginsconfig Document
     */  
    public static Document getPluginsConfig(){
        return pluginsconfig;
    }
        
    /* 
     * method to load plugins config from file to
     * pluginsconfig Node
     */
    public static boolean parsePluginsConfig(String filename){
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        try{DocumentBuilder db = dbf.newDocumentBuilder();
            File f = new File(filename);
            if(!f.exists())return false;
            Document doc = db.parse(f);
            doc.getDocumentElement().normalize();  
            pluginsconfig = doc;
            return true;
        }
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
    
    /*
     * method to copy plugins configuration file
     * to server 
     */
    public static boolean uploadPluginsFile(){
        try{
            DOMSource source = new DOMSource(pluginsconfig);
            File file = new File(Repository.PLUGINSLOCALGENERALCONF);
            Result result = new StreamResult(file);
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            transformer.transform(source, result);
            Repository.c.cd(Repository.USERHOME+"/twister/config/");
            System.out.println("Saving to: "+Repository.USERHOME+"/twister/config/");
            FileInputStream in = new FileInputStream(file);
            Repository.c.put(in, file.getName());
            in.close();
            return true;}
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
        
    /*
     * method to copy plugins configuration file
     * localy 
     */
    public static boolean getPluginsFile(){
        try{InputStream in = null;
            byte[] data = new byte[100]; 
            int nRead;
            ByteArrayOutputStream buffer = new ByteArrayOutputStream();
            OutputStream out=null;
            InputStreamReader inputStreamReader = null;
            BufferedReader bufferedReader = null;  
            BufferedWriter writer=null;
            File file;
            String line = null;
            String name = null;
            System.out.println("Starting getting plugins.xml from "+USERHOME+"/twister/config/");
            try{c.cd(USERHOME+"/twister/config/");}
            catch(Exception e){
                System.out.println("Could not get :"+USERHOME+"/twister/config/");
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,Repository.window,
                                        "Warning", "Could not get :"+USERHOME+
                                        "/twister/config/");
                return false;}
            try{System.out.println("plugins.xml size on sftp: "+
                        c.lstat("plugins.xml").getSize()+" bytes");
                in = c.get("plugins.xml");}
            catch(Exception e){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Repository.window,
                                        "Warning","Could not get plugins.xml from "+
                                        c.pwd());
                System.out.println("Could not get plugins.xml from "+
                                        c.pwd());
                return false;}
            inputStreamReader = new InputStreamReader(in);
            bufferedReader = new BufferedReader(inputStreamReader);  
            file = new File(PLUGINSLOCALGENERALCONF);
            writer = new BufferedWriter(new FileWriter(file));
            while((line=bufferedReader.readLine())!= null){
                writer.write(line);
                writer.newLine();}
            bufferedReader.close();
            writer.close();
            inputStreamReader.close();
            in.close();
            System.out.println("plugins.xml local size: "+file.length()+" bytes");
            intro.setStatus("Finished getting plugins");
            intro.repaint();
            return true;
        }
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
}    