{% extends "base.xml.tpl" %}
{% block headers %}<defaultcontrol>500</defaultcontrol>{% endblock %}
{% block controls %}
<control type="image">
    <width>1920</width>
    <height>{{ vscale(1080) }}</height>
    <texture colordiffuse="D0111111">script.plex/white-square.png</texture>
</control>
<control type="label">
    <posx>340</posx>
    <posy>{{ vscale(292) }}</posy>
    <width>1240</width>
    <height>{{ vscale(70) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <label>$ADDON[script.plexmod 35137]</label>
</control>
<control type="button" id="500">
    <posx>340</posx>
    <posy>{{ vscale(395) }}</posy>
    <width>185</width>
    <height>{{ vscale(185) }}</height>
    <font>font10</font>
    <textcolor>FFFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label />
    <onleft>505</onleft>
    <onright>501</onright>
    <onup>507</onup>
    <ondown>506</ondown>
</control>
<control type="image">
    <posx>377</posx>
    <posy>{{ vscale(422) }}</posy>
    <width>110</width>
    <height>{{ vscale(110) }}</height>
    <aspectratio>keep</aspectratio>
    <texture>script.plex/reactions/like.png</texture>
</control>
<control type="label">
    <posx>360</posx>
    <posy>{{ vscale(590) }}</posy>
    <width>180</width>
    <height>{{ vscale(40) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <label>$INFO[Window.Property(label.LIKE)]</label>
</control>
<control type="image">
    <visible>!String.IsEmpty(Window.Property(selected.LIKE))</visible>
    <posx>337</posx>
    <posy>{{ vscale(392) }}</posy>
    <width>191</width>
    <height>{{ vscale(191) }}</height>
    <texture border="12" colordiffuse="FFE5A00D">script.plex/white-outline-rounded.png</texture>
</control>
<control type="button" id="501">
    <posx>550</posx>
    <posy>{{ vscale(395) }}</posy>
    <width>185</width>
    <height>{{ vscale(185) }}</height>
    <font>font10</font>
    <textcolor>FFFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label />
    <onleft>500</onleft>
    <onright>502</onright>
    <onup>507</onup>
    <ondown>506</ondown>
</control>
<control type="image">
    <posx>587</posx>
    <posy>{{ vscale(422) }}</posy>
    <width>110</width>
    <height>{{ vscale(110) }}</height>
    <aspectratio>keep</aspectratio>
    <texture>script.plex/reactions/dislike.png</texture>
</control>
<control type="label">
    <posx>570</posx>
    <posy>{{ vscale(590) }}</posy>
    <width>180</width>
    <height>{{ vscale(40) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <label>$INFO[Window.Property(label.DISLIKE)]</label>
</control>
<control type="image">
    <visible>!String.IsEmpty(Window.Property(selected.DISLIKE))</visible>
    <posx>547</posx>
    <posy>{{ vscale(392) }}</posy>
    <width>191</width>
    <height>{{ vscale(191) }}</height>
    <texture border="12" colordiffuse="FFE5A00D">script.plex/white-outline-rounded.png</texture>
</control>
<control type="button" id="502">
    <posx>760</posx>
    <posy>{{ vscale(395) }}</posy>
    <width>185</width>
    <height>{{ vscale(185) }}</height>
    <font>font10</font>
    <textcolor>FFFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label />
    <onleft>501</onleft>
    <onright>503</onright>
    <onup>507</onup>
    <ondown>506</ondown>
</control>
<control type="image">
    <posx>797</posx>
    <posy>{{ vscale(422) }}</posy>
    <width>110</width>
    <height>{{ vscale(110) }}</height>
    <aspectratio>keep</aspectratio>
    <texture>script.plex/reactions/love.png</texture>
</control>
<control type="label">
    <posx>780</posx>
    <posy>{{ vscale(590) }}</posy>
    <width>180</width>
    <height>{{ vscale(40) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <label>$INFO[Window.Property(label.LOVE)]</label>
</control>
<control type="image">
    <visible>!String.IsEmpty(Window.Property(selected.LOVE))</visible>
    <posx>757</posx>
    <posy>{{ vscale(392) }}</posy>
    <width>191</width>
    <height>{{ vscale(191) }}</height>
    <texture border="12" colordiffuse="FFE5A00D">script.plex/white-outline-rounded.png</texture>
</control>
<control type="button" id="503">
    <posx>970</posx>
    <posy>{{ vscale(395) }}</posy>
    <width>185</width>
    <height>{{ vscale(185) }}</height>
    <font>font10</font>
    <textcolor>FFFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label />
    <onleft>502</onleft>
    <onright>504</onright>
    <onup>507</onup>
    <ondown>506</ondown>
</control>
<control type="image">
    <posx>1007</posx>
    <posy>{{ vscale(422) }}</posy>
    <width>110</width>
    <height>{{ vscale(110) }}</height>
    <aspectratio>keep</aspectratio>
    <texture>script.plex/reactions/laugh.png</texture>
</control>
<control type="label">
    <posx>990</posx>
    <posy>{{ vscale(590) }}</posy>
    <width>180</width>
    <height>{{ vscale(40) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <label>$INFO[Window.Property(label.LAUGH)]</label>
</control>
<control type="image">
    <visible>!String.IsEmpty(Window.Property(selected.LAUGH))</visible>
    <posx>967</posx>
    <posy>{{ vscale(392) }}</posy>
    <width>191</width>
    <height>{{ vscale(191) }}</height>
    <texture border="12" colordiffuse="FFE5A00D">script.plex/white-outline-rounded.png</texture>
</control>
<control type="button" id="504">
    <posx>1180</posx>
    <posy>{{ vscale(395) }}</posy>
    <width>185</width>
    <height>{{ vscale(185) }}</height>
    <font>font10</font>
    <textcolor>FFFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label />
    <onleft>503</onleft>
    <onright>505</onright>
    <onup>507</onup>
    <ondown>506</ondown>
</control>
<control type="image">
    <posx>1217</posx>
    <posy>{{ vscale(422) }}</posy>
    <width>110</width>
    <height>{{ vscale(110) }}</height>
    <aspectratio>keep</aspectratio>
    <texture>script.plex/reactions/applaud.png</texture>
</control>
<control type="label">
    <posx>1200</posx>
    <posy>{{ vscale(590) }}</posy>
    <width>180</width>
    <height>{{ vscale(40) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <label>$INFO[Window.Property(label.APPLAUD)]</label>
</control>
<control type="image">
    <visible>!String.IsEmpty(Window.Property(selected.APPLAUD))</visible>
    <posx>1177</posx>
    <posy>{{ vscale(392) }}</posy>
    <width>191</width>
    <height>{{ vscale(191) }}</height>
    <texture border="12" colordiffuse="FFE5A00D">script.plex/white-outline-rounded.png</texture>
</control>
<control type="button" id="505">
    <posx>1390</posx>
    <posy>{{ vscale(395) }}</posy>
    <width>185</width>
    <height>{{ vscale(185) }}</height>
    <font>font10</font>
    <textcolor>FFFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label />
    <onleft>504</onleft>
    <onright>500</onright>
    <onup>507</onup>
    <ondown>506</ondown>
</control>
<control type="image">
    <posx>1427</posx>
    <posy>{{ vscale(422) }}</posy>
    <width>110</width>
    <height>{{ vscale(110) }}</height>
    <aspectratio>keep</aspectratio>
    <texture>script.plex/reactions/question.png</texture>
</control>
<control type="label">
    <posx>1410</posx>
    <posy>{{ vscale(590) }}</posy>
    <width>180</width>
    <height>{{ vscale(40) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <label>$INFO[Window.Property(label.QUESTION)]</label>
</control>
<control type="image">
    <visible>!String.IsEmpty(Window.Property(selected.QUESTION))</visible>
    <posx>1387</posx>
    <posy>{{ vscale(392) }}</posy>
    <width>191</width>
    <height>{{ vscale(191) }}</height>
    <texture border="12" colordiffuse="FFE5A00D">script.plex/white-outline-rounded.png</texture>
</control>
<control type="button" id="506">
    <visible>!String.IsEmpty(Window.Property(has.reaction))</visible>
    <posx>680</posx>
    <posy>{{ vscale(705) }}</posy>
    <width>340</width>
    <height>{{ vscale(60) }}</height>
    <font>font10</font>
    <textcolor>FFFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$ADDON[script.plexmod 35145]</label>
    <onleft>507</onleft>
    <onright>507</onright>
    <onup>500</onup>
    <ondown>507</ondown>
</control>
<control type="button" id="507">
    <posx>1050</posx>
    <posy>{{ vscale(705) }}</posy>
    <width>200</width>
    <height>{{ vscale(60) }}</height>
    <font>font10</font>
    <textcolor>FFFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$ADDON[script.plexmod 35135]</label>
    <onleft>506</onleft>
    <onright>506</onright>
    <onup>500</onup>
    <ondown>500</ondown>
</control>{% endblock %}
