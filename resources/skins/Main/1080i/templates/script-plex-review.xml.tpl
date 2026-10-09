{% extends "default.xml.tpl" %}
{% block header %}{% endblock %}
{% block headers %}
<defaultcontrol>152</defaultcontrol>
{% endblock %}
{% block content %}
<control type="image">
    <posx>60</posx>
    <posy>{{ vscale(166) }}</posy>
    <width>520</width>
    <height>{{ vscale(292) }}</height>
    <aspectratio>keep</aspectratio>
    <texture background="true">$INFO[Window.Property(poster)]</texture>
    <colordiffuse>FFFFFFFF</colordiffuse>
</control>
<control type="label">
    <posx>60</posx>
    <posy>{{ vscale(482) }}</posy>
    <width>530</width>
    <height>{{ vscale(90) }}</height>
    <font>font13</font>
    <textcolor>FFFFFFFF</textcolor>
    <align>left</align>
    <label>$INFO[Window.Property(title)]</label>
</control>
<control type="label">
    <posx>60</posx>
    <posy>{{ vscale(582) }}</posy>
    <width>530</width>
    <height>{{ vscale(40) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <align>left</align>
    <label>$INFO[Window.Property(year)]</label>
</control>
<control type="textbox">
    <posx>60</posx>
    <posy>{{ vscale(652) }}</posy>
    <width>530</width>
    <height>{{ vscale(228) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <label>$INFO[Window.Property(summary)]</label>
</control>
<control type="image">
    <posx>680</posx>
    <posy>{{ vscale(160) }}</posy>
    <width>1140</width>
    <height>{{ vscale(545) }}</height>
    <texture border="12">script.plex/white-square-rounded.png</texture>
    <colordiffuse>B0181D24</colordiffuse>
</control>
<control type="image">
    <posx>705</posx>
    <posy>{{ vscale(182) }}</posy>
    <width>80</width>
    <height>{{ vscale(80) }}</height>
    <texture diffuse="script.plex/masks/role.png">script.plex/thumb_fallbacks/role.png</texture>
    <colordiffuse>FFFFFFFF</colordiffuse>
</control>
<control type="image">
    <posx>705</posx>
    <posy>{{ vscale(182) }}</posy>
    <width>80</width>
    <height>{{ vscale(80) }}</height>
    <texture background="true" diffuse="script.plex/masks/role.png">$INFO[Window.Property(avatar)]</texture>
    <colordiffuse>FFFFFFFF</colordiffuse>
</control>
<control type="label">
    <posx>810</posx>
    <posy>{{ vscale(186) }}</posy>
    <width>920</width>
    <height>{{ vscale(40) }}</height>
    <font>font12</font>
    <textcolor>FFFFFFFF</textcolor>
    <align>left</align>
    <label>$INFO[Window.Property(author)]</label>
</control>
<control type="label">
    <posx>810</posx>
    <posy>{{ vscale(230) }}</posy>
    <width>920</width>
    <height>{{ vscale(34) }}</height>
    <font>font10</font>
    <textcolor>99FFFFFF</textcolor>
    <align>left</align>
    <label>$INFO[Window.Property(date)]</label>
</control>
<control type="image">
    <posx>1070</posx>
    <posy>{{ vscale(284) }}</posy>
    <width>320</width>
    <height>{{ vscale(55) }}</height>
    <aspectratio>keep</aspectratio>
    <texture>$INFO[Window.Property(star.texture)]</texture>
</control>
<control type="textbox">
    <posx>710</posx>
    <posy>{{ vscale(354) }}</posy>
    <width>1040</width>
    <height>{{ vscale(270) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <label>$INFO[Window.Property(review)]</label>
    <pagecontrol>152</pagecontrol>
</control>
<control type="scrollbar" id="152">
    <posx>1770</posx>
    <posy>{{ vscale(354) }}</posy>
    <width>8</width>
    <height>{{ vscale(270) }}</height>
    <texturesliderbackground colordiffuse="33000000">script.plex/white-square.png</texturesliderbackground>
    <texturesliderbar colordiffuse="77FFFFFF">script.plex/white-square.png</texturesliderbar>
    <texturesliderbarfocus colordiffuse="FFFFFFFF">script.plex/white-square.png</texturesliderbarfocus>
    <textureslidernib>-</textureslidernib>
    <textureslidernibfocus>-</textureslidernibfocus>
    <orientation>vertical</orientation>
    <showonepage>true</showonepage>
    <ondown>310</ondown>
    <onleft>307</onleft>
    <onright>311</onright>
</control>
<control type="label">
    <visible>String.IsEmpty(Window.Property(is.reply))</visible>
    <posx>700</posx>
    <posy>{{ vscale(718) }}</posy>
    <width>900</width>
    <height>{{ vscale(46) }}</height>
    <font>font12</font>
    <textcolor>FFFFFFFF</textcolor>
    <align>left</align>
    <label>$INFO[Window.Property(discussion)]</label>
</control>
<control type="list" id="410">
    <posx>680</posx>
    <posy>{{ vscale(773) }}</posy>
    <width>1140</width>
    <height>{{ vscale(222) }}</height>
    <orientation>vertical</orientation>
    <onup>310</onup>
    <ondown>306</ondown>
    <onleft>307</onleft>
    <onright>308</onright>
    <scrolltime>150</scrolltime>
    <itemlayout width="1140" height="{{ vscale(180) }}">
        <control type="image">
            <posx>0</posx>
            <posy>{{ vscale(0) }}</posy>
            <width>1140</width>
            <height>{{ vscale(168) }}</height>
            <texture border="12">script.plex/white-square-rounded.png</texture>
            <colordiffuse>B0181D24</colordiffuse>
        </control>
        <control type="image">
            <posx>24</posx>
            <posy>{{ vscale(18) }}</posy>
            <width>48</width>
            <height>{{ vscale(48) }}</height>
            <texture background="true" diffuse="script.plex/masks/role.png">$INFO[ListItem.Thumb]</texture>
            <colordiffuse>FFFFFFFF</colordiffuse>
        </control>
        <control type="label">
            <posx>88</posx>
            <posy>{{ vscale(14) }}</posy>
            <width>1000</width>
            <height>{{ vscale(32) }}</height>
            <font>font10</font>
            <textcolor>DDFFFFFF</textcolor>
            <align>left</align>
            <label>$INFO[ListItem.Label]</label>
        </control>
        <control type="label">
            <posx>88</posx>
            <posy>{{ vscale(46) }}</posy>
            <width>1000</width>
            <height>{{ vscale(30) }}</height>
            <font>font10</font>
            <textcolor>99FFFFFF</textcolor>
            <align>left</align>
            <label>$INFO[ListItem.Label2]</label>
        </control>
        <control type="textbox">
            <posx>25</posx>
            <posy>{{ vscale(87) }}</posy>
            <width>1080</width>
            <height>{{ vscale(67) }}</height>
            <font>font10</font>
            <textcolor>DDFFFFFF</textcolor>
            <label>$INFO[ListItem.Property(text)]</label>
        </control>
    </itemlayout>
    <focusedlayout width="1140" height="{{ vscale(180) }}">
        <control type="image">
            <posx>0</posx>
            <posy>{{ vscale(0) }}</posy>
            <width>1140</width>
            <height>{{ vscale(168) }}</height>
            <texture border="12">script.plex/white-square-rounded.png</texture>
            <colordiffuse>B0181D24</colordiffuse>
        </control>
        <control type="image">
            <posx>24</posx>
            <posy>{{ vscale(18) }}</posy>
            <width>48</width>
            <height>{{ vscale(48) }}</height>
            <texture background="true" diffuse="script.plex/masks/role.png">$INFO[ListItem.Thumb]</texture>
            <colordiffuse>FFFFFFFF</colordiffuse>
        </control>
        <control type="label">
            <posx>88</posx>
            <posy>{{ vscale(14) }}</posy>
            <width>1000</width>
            <height>{{ vscale(32) }}</height>
            <font>font10</font>
            <textcolor>DDFFFFFF</textcolor>
            <align>left</align>
            <label>$INFO[ListItem.Label]</label>
        </control>
        <control type="label">
            <posx>88</posx>
            <posy>{{ vscale(46) }}</posy>
            <width>1000</width>
            <height>{{ vscale(30) }}</height>
            <font>font10</font>
            <textcolor>99FFFFFF</textcolor>
            <align>left</align>
            <label>$INFO[ListItem.Label2]</label>
        </control>
        <control type="textbox">
            <posx>25</posx>
            <posy>{{ vscale(87) }}</posy>
            <width>1080</width>
            <height>{{ vscale(67) }}</height>
            <font>font10</font>
            <textcolor>DDFFFFFF</textcolor>
            <label>$INFO[ListItem.Property(text)]</label>
        </control>
        <control type="image">
            <visible>Control.HasFocus(410)</visible>
            <posx>0</posx>
            <posy>{{ vscale(0) }}</posy>
            <width>1140</width>
            <height>{{ vscale(168) }}</height>
            <texture border="12">script.plex/white-outline-rounded.png</texture>
            <colordiffuse>FFFFFFFF</colordiffuse>
        </control>
    </focusedlayout>
</control>
<control type="label">
    <posx>700</posx>
    <posy>{{ vscale(802) }}</posy>
    <width>1100</width>
    <height>{{ vscale(56) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <align>left</align>
    <label>$INFO[Window.Property(comment.status)]</label>
</control>
<control type="button" id="307">
    <posx>60</posx>
    <posy>{{ vscale(65) }}</posy>
    <width>180</width>
    <height>{{ vscale(52) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$ADDON[script.plexmod 35135]</label>
    <onleft>308</onleft>
    <onright>308</onright>
    <ondown>152</ondown>
    <onup>152</onup>
</control>
<control type="button" id="308">
    <visible>String.IsEmpty(Window.Property(is.reply))</visible>
    <posx>1380</posx>
    <posy>{{ vscale(65) }}</posy>
    <width>240</width>
    <height>{{ vscale(52) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$ADDON[script.plexmod 35136]</label>
    <onleft>307</onleft>
    <onright>307</onright>
    <ondown>152</ondown>
    <onup>152</onup>
</control>
<control type="button" id="305">
    <posx>900</posx>
    <posy>{{ vscale(1008) }}</posy>
    <width>200</width>
    <height>{{ vscale(52) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$ADDON[script.plexmod 35111]</label>
    <onleft>307</onleft>
    <onright>306</onright>
    <ondown>410</ondown>
    <onup>152</onup>
    <visible>!String.IsEmpty(Window.Property(has.previous))</visible>
</control>
<control type="button" id="306">
    <posx>1120</posx>
    <posy>{{ vscale(1008) }}</posy>
    <width>200</width>
    <height>{{ vscale(52) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$ADDON[script.plexmod 35110]</label>
    <onleft>305</onleft>
    <onright>308</onright>
    <ondown>410</ondown>
    <onup>152</onup>
    <visible>!String.IsEmpty(Window.Property(has.next))</visible>
</control>

<control type="group">
    <visible>String.IsEmpty(Window.Property(is.reply))</visible>
    <control type="button" id="310">
        <posx>710</posx>
        <posy>{{ vscale(642) }}</posy>
        <width>190</width>
        <height>{{ vscale(52) }}</height>
        <font>font10</font>
        <textcolor>FFFFFFFF</textcolor>
        <focusedcolor>FF111111</focusedcolor>
        <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
        <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
        <label>$INFO[Window.Property(reaction.action)]</label>
        <onleft>307</onleft>
        <onright>311</onright>
        <onup>152</onup>
        <ondown>410</ondown>
        <enable>!String.IsEmpty(Window.Property(reaction.known)) + String.IsEmpty(Window.Property(reaction.busy))</enable>
        <align>left</align>
        <textoffsetx>55</textoffsetx>
    </control>
    <control type="button" id="311">
        <posx>920</posx>
        <posy>{{ vscale(642) }}</posy>
        <width>180</width>
        <height>{{ vscale(52) }}</height>
        <font>font10</font>
        <textcolor>FFFFFFFF</textcolor>
        <focusedcolor>FF111111</focusedcolor>
        <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
        <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
        <label>$ADDON[script.plexmod 35144]</label>
        <onleft>310</onleft>
        <onright>312</onright>
        <onup>152</onup>
        <ondown>410</ondown>
        <enable>String.IsEmpty(Window.Property(reaction.busy))</enable>
    </control>
    <control type="button" id="312">
        <posx>1500</posx>
        <posy>{{ vscale(642) }}</posy>
        <width>280</width>
        <height>{{ vscale(52) }}</height>
        <font>font10</font>
        <textcolor>FFFFFFFF</textcolor>
        <focusedcolor>FF111111</focusedcolor>
        <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
        <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
        <label>$ADDON[script.plexmod 35145]</label>
        <onleft>311</onleft>
        <onright>307</onright>
        <onup>152</onup>
        <ondown>410</ondown>
        <enable>!String.IsEmpty(Window.Property(reaction.known)) + String.IsEmpty(Window.Property(reaction.busy))</enable>
        <visible>!String.IsEmpty(Window.Property(reaction.mine))</visible>
    </control>
    <control type="image">
        <posx>718</posx>
        <posy>{{ vscale(650) }}</posy>
        <width>36</width>
        <height>{{ vscale(36) }}</height>
        <aspectratio>keep</aspectratio>
        <texture>$INFO[Window.Property(reaction.current.icon)]</texture>
    </control>
    {% for i in range(3) %}
    <control type="image">
        <posx>{{ 1120 + i * 38 }}</posx>
        <posy>{{ vscale(650) }}</posy>
        <width>40</width>
        <height>{{ vscale(40) }}</height>
        <aspectratio>keep</aspectratio>
        <texture>$INFO[Window.Property(reaction.icon.{{ i }})]</texture>
    </control>
    {% endfor %}
    <control type="label">
        <posx>1250</posx>
        <posy>{{ vscale(647) }}</posy>
        <width>220</width>
        <height>{{ vscale(44) }}</height>
        <font>font10</font>
        <textcolor>DDFFFFFF</textcolor>
        <label>$INFO[Window.Property(reaction.count)]</label>
    </control>
</control>
{% endblock %}
