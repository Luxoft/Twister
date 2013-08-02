/*
File: PluginManager.java ; This file is part of Twister.
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
import com.twister.plugin.twisterinterface.CommonInterface;
import java.io.File;

public class PluginManager implements CommonInterface{
    
    public void loadComponent(String comp){
        if(comp.equals("reports")){
            MainRepository.loadReports();
        } else if(comp.equals("login")){
            MainRepository.applet.init();
        } else {
//             File f = MainRepository.getRemoteFile(comp+".jar");
//             MainRepository.loadPlugin(f, comp);
            MainRepository.loadPlugin(comp);
        }
    }
    
    public void downloadJar(String comp){
    }
}
