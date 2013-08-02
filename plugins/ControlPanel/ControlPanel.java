/*
File: ControlPanel.java ; This file is part of Twister.
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


import java.applet.Applet;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Hashtable;

import javax.imageio.ImageIO;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import com.twister.Item;
import com.twister.plugin.baseplugin.BasePlugin;
import com.twister.plugin.twisterinterface.CommonInterface;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import org.w3c.dom.Document;

public class ControlPanel extends BasePlugin implements TwisterPluginInterface {
	private static final long serialVersionUID = 1L;
	private JPanel p;
	private CommonInterface maincomp;
	private Icon background,reports,runner,reportst,texec,um,tum;

	@Override
	public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
			final Hashtable<String, String> variables,
			final Document pluginsConfig,Applet applet) {
		super.init(suite, suitetest, variables, pluginsConfig,applet);
		System.out.println("Initializing " + getName() + " ... ");	
		
//		try {
//			InputStream in = getClass().getResourceAsStream("background.png");
//			Image im = ImageIO.read(in);
//			background = new ImageIcon(im);
//			in = getClass().getResourceAsStream("reports.png");
//			im = ImageIO.read(in);
//			reports = new ImageIcon(im);
//			in = getClass().getResourceAsStream("runner.png");
//			im = ImageIO.read(in);
//			runner = new ImageIcon(im);
//			in = getClass().getResourceAsStream("reportstxt.png");
//			im = ImageIO.read(in);
//			reportst = new ImageIcon(im);
//			in = getClass().getResourceAsStream("texec.png");
//			im = ImageIO.read(in);
//			texec = new ImageIcon(im);
//			in = getClass().getResourceAsStream("um.png");
//			im = ImageIO.read(in);
//			um = new ImageIcon(im);
//			in = getClass().getResourceAsStream("tum.png");
//			im = ImageIO.read(in);
//			tum = new ImageIcon(im);
//		} catch (Exception e){
//			e.printStackTrace();
//		}
		p = new JPanel();
//		p.setBackground(Color.GRAY);
//		
//		JPanel pn = new JPanel();
//		
//		JLabel l = new JLabel(background);
//		l.setBounds(10,100,175,311);
//		pn.add(l);
//		
//		l = new JLabel(reports);
//		l.setBounds(300,160,121,91);
//		pn.add(l);
//		
//		l = new JLabel(reportst);
//		l.setBounds(300,270,121,91);
//		pn.add(l);
//		
//		l = new JLabel(runner);
//		l.setBounds(500,150,121,110);
//		pn.add(l);
//
//		l = new JLabel(texec);
//		l.setBounds(500,290,140,60);
//		pn.add(l);
//		
//		
//		l = new JLabel(um);
//		l.setBounds(700,150,127,120);
//		pn.add(l);
//
//		l = new JLabel(tum);
//		l.setBounds(700,290,191,68);
//		pn.add(l);
//		
//		pn.setLayout(null);
//		pn.setPreferredSize(new Dimension(950,480));
//		
//		
//		p.setLayout(new GridBagLayout());
//		p.add(pn, new GridBagConstraints());
		
		
		
		
		try{
			String [] permissions = variables.get("permissions").split(",");
			Arrays.sort(permissions);
			if(Arrays.binarySearch(permissions, "CHANGE_USERS")>-1){
				JButton usermanagement = new JButton("User Management");
				usermanagement.setPreferredSize(new Dimension(150,30));
				p.add(usermanagement);
				usermanagement.addActionListener(new ActionListener() {
					@Override
					public void actionPerformed(ActionEvent e) {
						maincomp.loadComponent("UserManagement");
					}
				});
			}
		} catch(Exception e){
			e.printStackTrace();
		}
		
		
		JButton reports = new JButton("Reports");
		reports.setPreferredSize(new Dimension(150,30));
		p.add(reports);
		reports.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				maincomp.loadComponent("reports");
			}
		});
		
		JButton tcrunner = new JButton("Test Case Execution");
		tcrunner.setPreferredSize(new Dimension(150,30));
		p.add(tcrunner);
		tcrunner.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				maincomp.loadComponent("runner");
			}
		});
		
		JButton logout = new JButton("Logout");
		logout.setPreferredSize(new Dimension(150,30));
		//p.add(logout);
		logout.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				maincomp.loadComponent("login");
			}
		});
		
		p.setLayout(new FlowLayout());
		p.setPreferredSize(new Dimension(200,150));
        p.setMaximumSize(new Dimension(200,150));
        p.setMinimumSize(new Dimension(200,150));
        try{applet.removeAll();
			applet.setLayout(new GridBagLayout());
			applet.add(p, new GridBagConstraints());
			applet.revalidate();
			applet.repaint();
        } catch (Exception e){
        	e.printStackTrace();
        }
		System.out.println("successful");
	}

	@Override
	public Component getContent() {
		return p;
	}

	@Override
	public void setInterface(CommonInterface arg0) {
		this.maincomp = arg0;
	}

	@Override
	public String getFileName() {
		String filename = "ControlPanel.jar";
		return filename;
	}

	@Override
	public void terminate() {
		super.terminate();
		p = null;
	}

	@Override
	public String getName(){
		String name = "ControlPanel";
		return name;
	}
	
	public static void main(String [] args){
		JFrame fr = new JFrame();
		fr.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		fr.setBounds(100,100,800,600);
		ControlPanel cp = new ControlPanel();
		Hashtable ht = new Hashtable<>();
		ht.put("user", "tscguest");
		ht.put("password", "tscguest");
		ht.put("centralengineport", "8000");
		ht.put("host", "tsc-server");
		cp.init(null, null, ht, null,null);
		fr.add(cp.getContent());
		fr.setVisible(true);
	}
	
}