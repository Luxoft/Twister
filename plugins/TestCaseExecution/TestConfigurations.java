/*
File: TestConfigurations.java ; This file is part of Twister.
Version: 2.003

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
import java.awt.Color;
import javax.swing.JSplitPane;
import java.awt.BorderLayout;
import javax.swing.SwingUtilities;
import java.awt.Dimension;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class TestConfigurations extends JPanel{
    public ConfigTree tree;
    public ConfigEditor cfgedit;
    public JButton save, saveas, close;
    

    public TestConfigurations(){
        setBorder(BorderFactory.createTitledBorder("Test Configurations"));
        setLayout(new BorderLayout());
        cfgedit = new ConfigEditor();
        tree = new ConfigTree();
        final JSplitPane sp = new JSplitPane();
        sp.setLeftComponent(tree);
        sp.setRightComponent(cfgedit.sutpanel);
        sp.setOrientation(JSplitPane.HORIZONTAL_SPLIT);
        sp.setResizeWeight(0.5);
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                sp.setResizeWeight(0.5);
            }
        });
        tree.setConfigEditor(cfgedit);
        cfgedit.setConfigTree(tree);
        final JSplitPane sp2 = new JSplitPane();
        sp2.setLeftComponent(sp);
        sp2.setRightComponent(cfgedit);
        sp2.setOrientation(JSplitPane.VERTICAL_SPLIT);
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                sp2.setResizeWeight(0.5);
            }
        });
        add(sp2,BorderLayout.CENTER);
    }
    
    
}