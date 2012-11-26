/*
File: RoundButton.java ; This file is part of Twister.

Copyright (C) 2012 , Luxoft

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
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Shape;
import java.awt.Color;
import java.awt.geom.Ellipse2D;
import javax.swing.JButton;
import java.awt.GradientPaint;
import java.awt.Point;
import java.awt.RenderingHints;

public class RoundButton extends JButton {
    Shape shape;
    int rad = 15;
    
    public RoundButton(String label) {
        super(label);
        setFocusPainted(false);
        setContentAreaFilled(false);}
        
    public void setRadius(int rad){
        this.rad = rad;
    }

    protected void paintComponent(Graphics g) { 
        Graphics2D g2 = (Graphics2D)g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, 
                            RenderingHints.VALUE_ANTIALIAS_ON);
        if (getModel().isRollover()){
            g2.setPaint(new GradientPaint(new Point(0, 10), Color.WHITE, 
                                          new Point(0, getHeight()+30), 
                                          new Color(119,133,255),true));}
        if(!getModel().isArmed()&&!getModel().isRollover()){
            g2.setPaint(new GradientPaint(new Point(0, 10), Color.WHITE, 
                                          new Point(0, getHeight()+30), 
                                          new Color(66,85,255),true));}
        g2.fillRoundRect(0, 0,getSize().width-1 ,getSize().height-1, rad, rad);
        super.paintComponent(g2);} 

    protected void paintBorder(Graphics g) {
        g.setColor(new Color(150,150,150));
        if(!getModel().isArmed()){
            g.drawRoundRect(1, 1,getSize().width-2 ,getSize().height-2, rad, rad);}}

    public boolean contains(int x, int y) {
        if (shape == null || !shape.getBounds().equals(getBounds())){
            shape = new Ellipse2D.Float(0,0,getWidth(), getHeight());}
        return shape.contains(x, y);}}