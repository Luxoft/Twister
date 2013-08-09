/*
File: ControlPanel.java ; This file is part of Twister.
Version: 2.002

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
import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GradientPaint;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Image;
import java.awt.LinearGradientPaint;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
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
	private Icon background,reports,runner,reportst,texec,um,tum,logout;
	private boolean canum = false;

	@Override
	public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
			final Hashtable<String, String> variables,
			final Document pluginsConfig,Applet applet) {
		super.init(suite, suitetest, variables, pluginsConfig,applet);
		System.out.println("Initializing " + getName() + " ... ");	
		try{
			String [] permissions = variables.get("permissions").split(",");
			Arrays.sort(permissions);
			if(Arrays.binarySearch(permissions, "CHANGE_USERS")>-1){
				canum = true;
			}
		} catch(Exception e){
			canum = false;
			e.printStackTrace();
		}
		
		try {
			InputStream in = getClass().getResourceAsStream("background.png");
			Image im = ImageIO.read(in);
			
			background = new ImageIcon(im);
			in = getClass().getResourceAsStream("reports.png");
			im = ImageIO.read(in);
			reports = new ImageIcon(im);
			in = getClass().getResourceAsStream("runner.png");
			im = ImageIO.read(in);
			runner = new ImageIcon(im);
			in = getClass().getResourceAsStream("logout.png");
			im = ImageIO.read(in);
			logout = new ImageIcon(im);
			in = getClass().getResourceAsStream("reportstxt.png");
			im = ImageIO.read(in);
			reportst = new ImageIcon(im.getScaledInstance(82, 21, Image.SCALE_SMOOTH));
			in = getClass().getResourceAsStream("texec.png");
			im = ImageIO.read(in);
			texec = new ImageIcon(im.getScaledInstance(103, 45, Image.SCALE_SMOOTH));
			in = getClass().getResourceAsStream("um.png");
			im = ImageIO.read(in);
			um = new ImageIcon(im);
			in = getClass().getResourceAsStream("tum.png");
			im = ImageIO.read(in);
			tum = new ImageIcon(im.getScaledInstance(142, 50, Image.SCALE_SMOOTH));
		} catch (Exception e){
			e.printStackTrace();
		}
		p = new JPanel(){
			public void paintComponent(Graphics g){
				super.paintComponent(g);
				Graphics2D g2d = (Graphics2D)g;
				float[] fractions = {0.0f,0.7f,1.0f};
				Color[] colors = {new Color(46,138,187),new Color(53,161,199),new Color(43,138,187)};
				LinearGradientPaint lgp = new LinearGradientPaint(0, 0, 0, getHeight(), fractions , colors);
				g2d.setPaint(lgp);
				g2d.fillRect(0, 0, getWidth(),getHeight());
			}
			
		};
		//p.setBackground(Color.GRAY);
		
		JPanel pn = new JPanel(){
			public void paintComponent(Graphics g){
				super.paintComponent(g);
				Graphics2D g2d = (Graphics2D)g;
				//float[] fractions = {0.0f,0.7f,1.0f};
				//Color[] colors = {new Color(46,138,187),new Color(53,161,199),new Color(43,138,187)};
				//LinearGradientPaint lgp = new LinearGradientPaint(0, 0, 0, getHeight(), fractions , colors);
				//g2d.setPaint(lgp);
				//g2d.fillRect(0, 0, getWidth(),getHeight());
				
				g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
				
				g2d.setStroke(new BasicStroke(4F)); 
				
				g2d.setColor(new Color(10,92,129));
				g2d.drawRoundRect(250, 115, 160, 220, 25, 25);
				
				g2d.setColor(new Color(31,112,139));
				g2d.fillRoundRect(250, 115, 160, 220, 25, 25);
				
				
				g2d.setColor(new Color(10,92,129));
				g2d.drawRoundRect(480, 115, 160, 220, 25, 25);
				
				g2d.setColor(new Color(31,112,139));
				g2d.fillRoundRect(480, 115, 160, 220, 25, 25);
				
				if(canum){
					g2d.setColor(new Color(10,92,129));
					g2d.drawRoundRect(710, 115, 160, 220, 25, 25);
					
					g2d.setColor(new Color(31,112,139));
					g2d.fillRoundRect(710, 115, 160, 220, 25, 25);
				}
				
				
				
			}
		};
		pn.setOpaque(false);
		
		JLabel l = new JLabel(background);
		l.setBounds(10,100,175,311);
		pn.add(l);
		
		final JLabel lrep = new JLabel(reports);
		lrep.setBounds(250,115,160,220);
		pn.add(lrep);
		lrep.addMouseListener(new MouseAdapter(){
			
			@Override
			public void mouseExited(MouseEvent e) {
				lrep.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
				
			}
			
			@Override
			public void mouseEntered(MouseEvent e) {
				lrep.setCursor(new Cursor(Cursor.HAND_CURSOR));
			}
			
			@Override
			public void mouseClicked(MouseEvent e) {
				reports();
				
			}
		});
		
		final JLabel lout = new JLabel(logout);
		lout.setBounds(850,410,92,111);
		pn.add(lout);
		lout.addMouseListener(new MouseAdapter(){
			
			@Override
			public void mouseExited(MouseEvent e) {
				lout.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
				
			}
			
			@Override
			public void mouseEntered(MouseEvent e) {
				lout.setCursor(new Cursor(Cursor.HAND_CURSOR));
			}
			
			@Override
			public void mouseClicked(MouseEvent e) {
				logout();
				
			}
		});
		
		l = new JLabel(reportst);
		l.setBounds(270,245,121,91);
		pn.add(l);
		
		final JLabel trunner  = new JLabel(runner);
		trunner.setBounds(480,115,160,220);
		pn.add(trunner);
		trunner.addMouseListener(new MouseAdapter(){
			
			@Override
			public void mouseExited(MouseEvent e) {
				trunner.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
				
			}
			
			@Override
			public void mouseEntered(MouseEvent e) {
				trunner.setCursor(new Cursor(Cursor.HAND_CURSOR));
			}
			
			@Override
			public void mouseClicked(MouseEvent e) {
				testexec();
			}
		});

		l = new JLabel(texec);
		l.setBounds(490,265,140,60);
		pn.add(l);
		
		
			if(canum){
				final JLabel lum = new JLabel(um);
				lum.setBounds(710, 115, 160, 220);
				pn.add(lum);
				lum.addMouseListener(new MouseAdapter(){
					
					@Override
					public void mouseExited(MouseEvent e) {
						lum.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
						
					}
					
					@Override
					public void mouseEntered(MouseEvent e) {
						lum.setCursor(new Cursor(Cursor.HAND_CURSOR));
					}
					
					@Override
					public void mouseClicked(MouseEvent e) {
						um();
					}
				});
				l = new JLabel(tum);
				l.setBounds(695,265,191,68);
				pn.add(l);
			}
		
		
		
		pn.setLayout(null);
		pn.setPreferredSize(new Dimension(950,550));
		
		
		p.setLayout(new GridBagLayout());
		p.add(pn, new GridBagConstraints());
		
//		try{
//			String [] permissions = variables.get("permissions").split(",");
//			Arrays.sort(permissions);
//			if(Arrays.binarySearch(permissions, "CHANGE_USERS")>-1){
//				JButton usermanagement = new JButton("User Management");
//				usermanagement.setPreferredSize(new Dimension(150,30));
//				p.add(usermanagement);
//				usermanagement.addActionListener(new ActionListener() {
//					@Override
//					public void actionPerformed(ActionEvent e) {
//						maincomp.loadComponent("UserManagement");
//					}
//				});
//			}
//		} catch(Exception e){
//			e.printStackTrace();
//		}
		
		
		JButton reports = new JButton("Reports");
		reports.setPreferredSize(new Dimension(150,30));
		//p.add(reports);
		reports.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				maincomp.loadComponent("reports");
			}
		});
		
		JButton tcrunner = new JButton("Test Case Execution");
		tcrunner.setPreferredSize(new Dimension(150,30));
		//p.add(tcrunner);
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
		
//		p.setLayout(new FlowLayout());
//		p.setPreferredSize(new Dimension(200,150));
//        p.setMaximumSize(new Dimension(200,150));
//        p.setMinimumSize(new Dimension(200,150));
        try{applet.removeAll();
			applet.setLayout(new BorderLayout());
			applet.add(p,BorderLayout.CENTER);
			//applet.add(p, new GridBagConstraints());
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
	
	private void logout(){
		maincomp.loadComponent("login");
		//System.out.println("logout");
	}
	
	private void reports(){
		//System.out.println("reports");
		maincomp.loadComponent("reports");
	}
	
	private void testexec(){
		//System.out.println("testexec");
		maincomp.loadComponent("runner");
	}
	
	private void um(){
		maincomp.loadComponent("UserManagement");
		//System.out.println("um");
	}
	
	public static void main(String [] args){
		JFrame fr = new JFrame();
		fr.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		fr.setBounds(100,100,800,600);
		ControlPanel cp = new ControlPanel();
		Hashtable ht = new Hashtable();
		ht.put("user", "tscguest");
		ht.put("password", "tscguest");
		ht.put("centralengineport", "8000");
		ht.put("host", "tsc-server");
		cp.init(null, null, ht, null,null);
		fr.add(cp.getContent());
		fr.setVisible(true);
	}
	
}