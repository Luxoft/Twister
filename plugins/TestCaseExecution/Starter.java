/*
File: Starter.java ; This file is part of Twister.
Version: 2.008

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
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import com.twister.plugin.twisterinterface.CommonInterface;
import com.twister.plugin.baseplugin.BasePlugin;
import java.util.ArrayList;
import java.util.Hashtable;
import com.twister.Item;
import org.w3c.dom.Document;
import java.applet.Applet;
import java.awt.Component;
import java.net.URL;
import java.awt.Image;
import javax.imageio.ImageIO;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.File;
import javax.imageio.IIOException;
import java.io.FileNotFoundException;

public class Starter implements TwisterPluginInterface{
    public CommonInterface maincomp;
    
    public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
            final Hashtable<String, String> variables,
            final Document pluginsConfig,Applet container) {
                RunnerRepository.starter = this;
                URL url = null;
                try {
                    url = new URL(container.getCodeBase()+"/logo.png");
                    RunnerRepository.logo = ImageIO.read(url).getScaledInstance(230, 100, Image.SCALE_FAST);
                } catch (IIOException e) {
                    System.out.println("Could not get image: "+url.toExternalForm());
                } catch (Exception e){
                    e.printStackTrace();
                }
                readLogoTxt(container);
                PermissionValidator.init(variables.get("permissions"));
                RunnerRepository.user = variables.get("user");
                RunnerRepository.password = variables.get("password");
                RunnerRepository.host = variables.get("host");
                container.removeAll();
                container.revalidate();
                container.repaint();
                RunnerRepository.initialize("true",variables.get("host"),container,container);
                resizePlugin((int)container.getSize().getWidth(),(int)container.getSize().getHeight());
    }
    
    public void readLogoTxt(Applet container){
        URL logo = null;
        try{
            logo = new URL(container.getCodeBase()+"/logo.txt");
            BufferedReader in = new BufferedReader(
            new InputStreamReader(logo.openStream()));
            
            StringBuilder sb = new StringBuilder();
            String inputLine;
            while ((inputLine = in.readLine()) != null){
                sb.append(inputLine);
                sb.append("\n");
            }
            in.close();
            RunnerRepository.logotxt = sb.toString();
        }catch(FileNotFoundException e){
            System.out.println("Could not get file: "+logo.toExternalForm());
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
    public String getFileName() {
        String filename = "runner.jar";
        return filename;
    }
    
    public String getDescription(String desc){
        return "";
    }
    
    /*
     * terminate method called
     * when exiting runner interface
     * all 
     */
    public void terminate(){
        System.out.println("Stopping TC Runner");
        RunnerRepository.saveMainLayout();
        File file = new File(RunnerRepository.temp);
        if(file.exists()){
            if(Window.deleteTemp(file))
                System.out.println(RunnerRepository.temp+" deleted successfull");
            else System.out.println("Could not delete: "+RunnerRepository.temp);}
        RunnerRepository.run = false;
        RunnerRepository.session.disconnect();
        RunnerRepository.connection.disconnect();        
        RunnerRepository.window.mainpanel.p1.ep.session.disconnect();
        RunnerRepository.window.mainpanel.p1.ep.connection.disconnect();
        RunnerRepository.window.mainpanel.p1.lp.session.disconnect();
        RunnerRepository.window.mainpanel.p1.lp.connection.disconnect();
        RunnerRepository.window.mainpanel.p4.getPlugins().session.disconnect();
        RunnerRepository.window.mainpanel.p4.getPlugins().ch.disconnect();
        RunnerRepository.window.mainpanel.p4.getGlobals().session.disconnect();
        RunnerRepository.window.mainpanel.p4.getGlobals().ch.disconnect();
        RunnerRepository.window.mainpanel.p4.getTestConfig().tree.session.disconnect();
        RunnerRepository.window.mainpanel.p4.getTestConfig().tree.connection.disconnect();
        RunnerRepository.window.mainpanel.p4.getTestConfig().cfgedit.session.disconnect();
        RunnerRepository.window.mainpanel.p4.getTestConfig().cfgedit.ch.disconnect();
    }
    
    public String getName(){
        String name = "runner";
        return name;
    }
    
    public Component getContent() {
        return RunnerRepository.window.mainpanel;
    }
    
    public void setInterface(CommonInterface arg0) {
        this.maincomp=arg0;
    }
    
    public void resizePlugin(int width, int height){
        RunnerRepository.setSize(width, height);
    }
}