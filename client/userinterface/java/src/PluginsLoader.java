/*
File: PluginsLoader.java ; This file is part of Twister.
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
import java.io.File;
import java.lang.reflect.Method;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.Iterator;
import java.util.ServiceLoader;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import java.io.InputStream;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class PluginsLoader {
    private static URLClassLoader sysLoader;
    private static Class[] parameters = new Class[]{URL.class};
    
    public static void setClassPath(){
        try{
            if(sysLoader==null){
                sysLoader= new URLClassLoader(new URL[]{},Plugins.class.getClassLoader());
            }
            addDirToClasspath(new File(Repository.PLUGINSDIRECTORY));
        }
        catch(Exception e){e.printStackTrace();}}
    
    public static Iterator<TwisterPluginInterface> getPlugins() {
        return ServiceLoader.load(TwisterPluginInterface.class,sysLoader).iterator();}
    
    public static void addDirToClasspath(File directory) throws Exception{
        if(directory.exists()){
            File[]files = directory.listFiles();
            for(int i=0;i<files.length;i++){
                File file = files[i];
                addURL(file.toURI().toURL());}}}
    
    public static void addURL(URL u) throws Exception{
        URL urls[] = sysLoader.getURLs();
        for(int i=0;i<urls.length;i++){
            if(urls[i].toString().equalsIgnoreCase(u.toString())){
                return;}}
        Class sysClass = URLClassLoader.class;
        try{Method method = sysClass.getDeclaredMethod("addURL", parameters);
            method.setAccessible(true);
            method.invoke(sysLoader, new Object[]{u});}
		catch(Exception e){e.printStackTrace();}}}
