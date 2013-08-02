/*
File: MainRepository.java ; This file is part of Twister.
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
import java.awt.Container;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.BorderLayout;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import java.awt.Image;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.net.URL;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import java.util.Properties;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.w3c.dom.Element;
import javax.swing.JOptionPane;
import com.twister.CustomDialog;
import java.util.HashMap;
import java.util.Vector;
import java.io.File;
import java.io.OutputStream;
import java.io.InputStream;
import java.io.FileOutputStream;
import java.util.Iterator;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import java.applet.Applet;
import java.util.Hashtable;
import java.awt.Component;

public class MainRepository {
    public static Image background;
    private static String host,user,password,ceport;
    public static Container container;
    public static String bar = System.getProperty("file.separator");//System specific file.separator
    public static String temp;
    private static ChannelSftp connection;
    private static PluginManager pluginmanager;
    public static Applet applet;
    private static TwisterPluginInterface plugin;
    private static XmlRpcClient client;
    private static Hashtable<String,String> hash = new Hashtable<String,String>();
    
    public static void initialize(Applet applet, String host,Container container){
        MainRepository.applet = applet;
        MainRepository.host = host;
        MainRepository.container = container;
        createDirectories();
        MainRepository.container = container;
        WelcomePanel wp = new WelcomePanel();
        container.removeAll();
        container.setBackground(wp.getBackground());
        container.setLayout(new GridBagLayout());
        container.add(wp, new GridBagConstraints());
        container.revalidate();
        container.repaint();
        PluginsLoader.setClassPath();
        pluginmanager = new PluginManager();
    }
    
    public static void resize(int width,int height){
        System.out.println("MainRepo resize");
        if(plugin!=null){
            System.out.println("plugin name: "+plugin.getName());
            try{plugin.resizePlugin(width,height);}
            catch(Exception e){e.printStackTrace();}
        } else {
            System.out.println("plugin is null");
        }
    }
    
    public static boolean isCE(){
        try{client.execute("echo", new Object[]{"test if CE is running"});
            return true;
        } catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
    
    private static void createDirectories(){
        try{
            temp = System.getProperty("user.home")+bar+".twister" ;
            File g1 = new File(temp);
            
            if(g1.mkdir()){
                System.out.println(temp+" successfully created");}
            else System.out.println(temp+" could not be created ");
            
            g1 = new File(temp+bar+host);
            if(g1.mkdir()){
                System.out.println(temp+bar+host+" successfully created");}
            else System.out.println(temp+bar+host+" could not be created ");
            
            temp = g1.getCanonicalPath();
            
            g1 = new File(temp+bar+"components");
            if(g1.exists())g1.delete();
            if(g1.mkdir()){
                System.out.println(temp+bar+host+bar+"components successfully created");}
            else System.out.println(temp+bar+host+bar+"components could not be created ");
        
        }
        catch(Exception e){
            System.out.println("Could not retrieve Temp directory for this OS");
            e.printStackTrace();}
        System.out.println("Temp directory where Twister Directory is created: "+temp);
        File file = new File(MainRepository.temp+bar+"Twister");
        File twisterhome = new File(System.getProperty("user.home")+bar+".twister");
    }
    
    public static void login(String user, String password){
        MainRepository.user = user;
        MainRepository.password = password;
        ceport = getCEPort(user,password);
        if(ceport==null)return;
        initializeRPC(user,password,ceport);
    }
    
    private static String getCEPort(String user, String password){
        try{DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            JSch jsch = new JSch();
            Session session = jsch.getSession(user, host, 22);
            session.setPassword(password);
            Properties config = new Properties();
            config.put("StrictHostKeyChecking", "no");
            session.setConfig(config);
            try{session.connect();}
            catch(Exception e){
                e.printStackTrace();
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,applet,
                                    "Warning", "Could not connect to server");
                return null;
            }
            Channel channel = session.openChannel("sftp");
            channel.connect();
            connection = (ChannelSftp)channel;
            Document doc = db.parse(connection.get(connection.getHome()+"/twister/config/fwmconfig.xml"));
            doc.getDocumentElement().normalize();
            String tag = "CentralEnginePort";
            NodeList nodeLst = doc.getElementsByTagName(tag);
            if(nodeLst.getLength()==0){
                System.out.println("tag "+tag+" not found in "+doc.getDocumentURI());
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,container,
                                            "Warning", tag+" tag not found in framework config");
                return "";
            }
            Node fstNode = nodeLst.item(0);
            Element fstElmnt = (Element)fstNode;
            NodeList fstNm = fstElmnt.getChildNodes();
            String temp;
            try{temp = fstNm.item(0).getNodeValue().toString();}
            catch(Exception e){
                System.out.println(tag+" empty");
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,MainRepository.container,
                                            "Warning", tag+" tag is empty in framework config");
                temp = "";}
            return temp;
        } catch(Exception e){
            e.printStackTrace();
        }
        return "";
    }
    
    public static void loadReports(){
        try{applet.getAppletContext().showDocument(new URL("http://"+user+":"+password+"@"+host+":"+
                                                    ceport+"/report/index/"+user), "_blank");}
        catch(Exception ex){ex.printStackTrace();}
    }
    
    
    
    public static void getInterface(String panel){
        if(panel.equals("controlpanel")){
            try{
//                 File file = getRemoteFile("ControlPanel.jar");
//                 loadPlugin(file,"ControlPanel");
                loadPlugin("ControlPanel");
            } catch(Exception e){
                e.printStackTrace();
            }
        }
    }
    
//     public static void loadPlugin(File file, String pluginname){
    public static void loadPlugin(String pluginname){
        try{
//             PluginsLoader.addDirToClasspath(file);
//             Iterator<TwisterPluginInterface> iterator = PluginsLoader.getPlugins();
//             String name;
//             while(iterator.hasNext()){
//                 try{plugin = iterator.next();}
//                 catch(Exception e){
//                     System.out.println("Could not instatiate plugin");
//                     e.printStackTrace();
//                     continue;}
//                 name = plugin.getName();
//                 if(name.equals(pluginname)){
//                     new Thread(){
//                         public void run(){
//                             hash.put("user", user);
//                             hash.put("password", password);
//                             hash.put("host",host);
//                             hash.put("centralengineport", ceport);
//                             plugin.init(null, null, hash, null,applet);
//                             plugin.setInterface(pluginmanager);
//                         }
//                     }.start();
//                     return;
//                 }
//             }

            if(pluginname.equals("ControlPanel")){
                new Thread(){
                    public void run(){
                        hash.put("user", user);
                        hash.put("password", password);
                        hash.put("host",host);
                        hash.put("centralengineport", ceport);
                        ControlPanel cp = new ControlPanel();
                        plugin = cp;
                        cp.init(null, null, hash, null,applet);
                        cp.setInterface(pluginmanager);
                    }
                }.start();
            } else if(pluginname.equals("UserManagement")){
                new Thread(){
                    public void run(){
                        hash.put("user", user);
                        hash.put("password", password);
                        hash.put("host",host);
                        hash.put("centralengineport", ceport);
                        UserManagement um = new UserManagement();
                        plugin = um;
                        um.init(null, null, hash, null,applet);
                        um.setInterface(pluginmanager);
                    }
                }.start();
            } else if(pluginname.equals("runner")){
                new Thread(){
                    public void run(){
                        hash.put("user", user);
                        hash.put("password", password);
                        hash.put("host",host);
                        hash.put("centralengineport", ceport);
                        Starter st = new Starter();
                        plugin  = st;
                        st.init(null, null, hash, null,applet);
                        st.setInterface(pluginmanager);
                    }
                }.start();
            }
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    
    public static File getRemoteFile(final String remotefile){
        try{
            InputStream in = connection.get("/opt/twister/appletcomps/"+remotefile);
            File file = new File(temp+bar+"components/"+remotefile);
            OutputStream out=new FileOutputStream(file);
            byte buf[]=new byte[100];
            int len;
            while((len=in.read(buf))>0)
                out.write(buf,0,len);
            out.close();
            in.close();
            return file;
        } catch (Exception e){
            e.printStackTrace();
            return null;
        }
    }
    
    /*
     * XmlRpc main connection used by Twister framework
     */
    public static void initializeRPC(String user, String password,String port){
        try{XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
            configuration.setBasicPassword(password);
            configuration.setBasicUserName(user);
            configuration.setServerURL(new URL("http://"+user+":"+password+"@"+MainRepository.host+
                                        ":"+port+"/"));
            System.out.println("http://"+user+":"+password+"@"+MainRepository.host+
                                        ":"+port+"/");
            client = new XmlRpcClient();
            client.setConfig(configuration);
            System.out.println("Client initialized: "+client);
            if(!isCE()){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,applet,
                                    "Warning", "CE is not running, please start CE in "+
                                                "order for Twister Framework to run properly");
                return;
            }
            HashMap hm = (HashMap)client.execute("usersAndGroupsManager", new Object[]{"list users"});
            hm = (HashMap)hm.get(user);
            if(hm==null){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,container,
                                        "Warning", "User: "+user+" is not present in users list, please add it to configuration file");
                return;        
            }
            Object [] permissions = (Object [])hm.get("roles");
            StringBuilder sb = new StringBuilder();
            for(Object ob:permissions){
                sb.append(ob.toString());
                sb.append(",");
            }
            if(sb.length()>0)sb.setLength(sb.length()-1);
            System.out.println("permissions:"+sb.toString());
            hash.put("permissions", sb.toString());
            loadPlugin("ControlPanel");
//             getInterface("controlpanel");
        }
        catch(Exception e){
            e.printStackTrace();
            System.out.println("Could not conect to "+
                            MainRepository.host+" :"+port+
                            "for RPC client initialization");
        }
    }
}