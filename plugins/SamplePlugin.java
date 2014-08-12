/*
File: SamplePlugin.java ; This file is part of Twister.

Copyright (C) 2012-2014 , Luxoft
Version: 1.001
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

import java.awt.Component;
import java.util.ArrayList;
import java.util.Hashtable;
import javax.swing.JLabel;
import javax.swing.JPanel;
import com.twister.Item;
import org.w3c.dom.Document;
import java.applet.Applet;
import com.twister.plugin.baseplugin.BasePlugin;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;

public class SamplePlugin extends BasePlugin implements TwisterPluginInterface {
    private static final long serialVersionUID = 1L;
    private JPanel p;
    private JLabel label;

    @Override
    public void init(ArrayList <Item>suite,ArrayList <Item>suitetest,
                     Hashtable<String, String>variables,
                     Document pluginsConfig, Applet container) {
        super.init(suite, suitetest, variables, pluginsConfig,container);
        p = new JPanel();
        // get the username from framework and display it in plugin tab
        label = new JLabel("I am user: "+variables.get("user"));
        p.add(label);
    }

    @Override
    public Component getContent() {
        return p;
    }

    @Override
    public String getDescription(String plugindir) {
        String description = "Shows the basic skeleton for a plugin";
        return description;
    }

    @Override
    public String getFileName() {
        String filename = "SamplePlugin.jar";
        return filename;
    }

    @Override
    public String getName() {
        String name = "SamplePlugin";
        return name;
    }

    @Override
    public void terminate() {
        super.terminate();
        p = null;
        label = null;
    }
}



