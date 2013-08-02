/*
File: Starter.java ; This file is part of Twister.
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

public class Starter implements TwisterPluginInterface{
    public CommonInterface maincomp;
    
    public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
            final Hashtable<String, String> variables,
            final Document pluginsConfig,Applet container) {
                RunnerRepository.starter = this;
                PermissionValidtor.init(variables.get("permissions"));
                RunnerRepository.user = variables.get("user");
                RunnerRepository.password = variables.get("password");
                RunnerRepository.host = variables.get("host");
                container.removeAll();
                container.revalidate();
                container.repaint();
                RunnerRepository.initialize("true",variables.get("host"),container);
                try{
                    container.getAppletContext().showDocument(new URL("javascript:resize()"));
                } catch (Exception e) {
                    System.err.println("Failed to call JavaScript function appletLoaded()");
                }
    }
    
    public String getFileName() {
        String filename = "runner.jar";
        return filename;
    }
    
    public String getDescription(String desc){
        return "";
    }
    
    public void terminate(){}
    
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
        System.out.println("Starter resizing");
        RunnerRepository.setSize(width, height);
    }
}