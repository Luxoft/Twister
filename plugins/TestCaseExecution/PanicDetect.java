/*
File: PanicDetect.java ; This file is part of Twister.
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
import javax.swing.BoxLayout;
import javax.swing.JTextField;
import javax.swing.JCheckBox;
import javax.swing.JButton;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyAdapter;
import java.awt.Container;
import java.util.HashMap;
import javax.swing.JLabel;
import com.google.gson.JsonParser;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;
import java.util.Iterator;
import java.util.Map;
import javax.swing.JOptionPane;
import com.twister.CustomDialog;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import javax.swing.event.DocumentListener;
import javax.swing.event.DocumentEvent;
import javax.swing.BorderFactory;
import java.awt.Color;

public class PanicDetect extends JPanel{
    private JButton add;
    private JPanel addpanel;
    
    public PanicDetect(){
        //setBorder(BorderFactory.createTitledBorder("Panic Detect"));
        setBackground(Color.WHITE);
        setLayout(new BoxLayout(this, BoxLayout.PAGE_AXIS));
        add = new JButton("Add");
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addRegex();
            }
        });
        add.setBounds(415,5,100,25);
        addpanel = new JPanel();
        addpanel.setBackground(Color.WHITE);
        addpanel.setPreferredSize(new Dimension(520, 35));
        addpanel.setMinimumSize(new Dimension(520, 35));
        addpanel.setMaximumSize(new Dimension(520, 35));
        addpanel.setLayout(null);
        addpanel.add(add);
        add(addpanel);
        listRegex();
    }
    
    private void listRegex(){
        try{
            String result = RunnerRepository.getRPCClient().execute("panicDetectConfig",
                                                                  new Object[]{RunnerRepository.getUser(),
                                                                               "list"}).toString();
            JsonElement jelement = new JsonParser().parse(result);
            JsonObject main = jelement.getAsJsonObject();
            JsonObject regex = main.getAsJsonObject(RunnerRepository.getUser());
            if(regex==null)return;
            Iterator <Map.Entry<String,JsonElement>> iter = regex.entrySet().iterator();
            while(iter.hasNext()){
                Map.Entry <String,JsonElement>n = iter.next();
                String id = n.getKey();
                JsonElement content = n.getValue();
                JsonObject ob = content.getAsJsonObject();
                String exp = ob.get("expression").getAsString();
                String en = ob.get("enabled").getAsString();
                MyPanel panel =new MyPanel(exp, Boolean.parseBoolean(en),id);
                addPanel(panel);
            }
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
    private void addRegex(){
        try{
            String result = RunnerRepository.getRPCClient().execute("panicDetectConfig",
                                                              new Object[]{RunnerRepository.getUser(),
                                                                           "add","expression=new_regex&enabled=false"}).toString();
            if(result.indexOf("error")==-1){
                MyPanel p = new MyPanel("new_regex",false,result);
                addPanel(p);    
                p.highlight();
            } else {
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,
                                      this,
                                      "Warning", result);
            }
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
    private void addPanel(JPanel p){
        add(p);
        remove(addpanel);
        add(addpanel);
        revalidate();
        repaint();
    }
    
    class MyPanel extends JPanel{
        private static final long serialVersionUID = 1L;
        private JTextField regex;
        private JCheckBox enabled;
        private JButton remove;
        private String id;
        
        public MyPanel(String regex, boolean enabled, String id) {
            this();
            this.regex.setText(regex);
            this.enabled.setSelected(enabled);
            this.id = id;
            this.enabled.setSelected(enabled);
            setBackground(Color.WHITE);
        }

        public MyPanel(){
            setLayout(null);
            setPreferredSize(new Dimension(620, 35));
            setMinimumSize(new Dimension(620, 35));
            setMaximumSize(new Dimension(620, 35));
            JLabel regexl = new JLabel("RegEx: ");
            regexl.setBackground(Color.WHITE);
            regexl.setBounds(10,5,60,25);
            add(regexl);
            regex = new JTextField();
            enabled = new JCheckBox("Enabled");
            enabled.setBackground(Color.WHITE);
            remove = new JButton("Remove");
            regex.setBounds(75, 5, 200, 25);
            add(regex);
            enabled.setBounds(330, 5, 100, 25);
            add(enabled);
            remove.setBounds(465, 5, 100, 25);
            add(remove);
            remove.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    removeRegex();
                }
            });
            enabled.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    if(regex.getText().equals("")){
                        enabled.setSelected(!enabled.isSelected());
                    }
                    regexModified();
                }
            });
            //send to CE modifications when focus is lost
            regex.addFocusListener(new FocusAdapter(){
                public void focusLost(FocusEvent ev){
                    if(regex.getText().equals("")){
                        try{
                            String result = RunnerRepository.getRPCClient().execute("panicDetectConfig",
                                                                      new Object[]{RunnerRepository.getUser(),
                                                                                   "list"}).toString();
                            JsonElement jelement = new JsonParser().parse(result);
                            JsonObject main = jelement.getAsJsonObject();
                            JsonObject reg = main.getAsJsonObject(RunnerRepository.getUser());
                            result = (((JsonObject)reg.get(id)).get("expression")).getAsString();
                            regex.setText(result);
                        } catch(Exception e){e.printStackTrace();}
                    }
                    regexModified();
                }
            });
            regex.addFocusListener(new FocusAdapter(){
                public void focusLost(FocusEvent ev){
                    if(regex.getText().equals("")){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,PanicDetect.this,
                                                      "Warning", "Regex must not be empty");
                        try{
                            String result = RunnerRepository.getRPCClient().execute("panicDetectConfig",
                                                                      new Object[]{RunnerRepository.getUser(),
                                                                                   "list"}).toString();
                            JsonElement jelement = new JsonParser().parse(result);
                            JsonObject main = jelement.getAsJsonObject();
                            JsonObject reg = main.getAsJsonObject(RunnerRepository.getUser());
                            result = ((JsonObject)reg.get(id)).get("expression").toString();
                            result = result.substring(1, result.length()-1);
                            regex.setText(result);
                        } catch(Exception e){e.printStackTrace();}
                        regex.requestFocusInWindow();
                        regex.requestFocus();
                        return;
                    }
                }
            });
        }
        
        //method to select all text, used after
        //new regex is added
        public void highlight(){
            regex.requestFocus();
            regex.requestFocusInWindow();
            regex.selectAll();
        }
        
        public void regexModified(){
            try{
                if(regex.getText().equals(""))return;
                String com = "expression="+regex.getText()+
                             "&enabled="+enabled.isSelected()+
                             "&id="+id;
                String result = RunnerRepository.getRPCClient().execute("panicDetectConfig",
                                                                    new Object[]{RunnerRepository.getUser(),
                                                                           "update",com}).toString();
            } catch (Exception e){
                e.printStackTrace();
            }
        }
        
        public void removeRegex(){
            try{
                if(regex.getText().equals(""))return;
                String result = RunnerRepository.getRPCClient().execute("panicDetectConfig",
                                                                   new Object[]{RunnerRepository.getUser(),
                                                                   "remove",id}).toString();
                if(result.equals("true")){
                    Container parent = getParent();
                    parent.remove(this);
                    parent.revalidate();
                    parent.repaint();
                } else {
                    CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,
                                          this,
                                          "Warning", result);
                }
            } catch(Exception e){
                e.printStackTrace();
            }
        }

        public String getRegex() {
            return regex.getText();
        }

        public void setRegex(String regex) {
            this.regex.setText(regex);
        }

        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }
    }
}
