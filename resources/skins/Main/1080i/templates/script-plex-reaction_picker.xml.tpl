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
{% for i, kind in [(0, "like"), (1, "dislike"), (2, "love"), (3, "laugh"), (4, "applaud"), (5, "question")] %}
<control type="button" id="{{ 500 + i }}">
    <posx>{{ 340 + i * 210 }}</posx>
    <posy>{{ vscale(395) }}</posy>
    <width>185</width>
    <height>{{ vscale(185) }}</height>
    <font>font10</font>
    <textcolor>FFFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label />
    <onleft>{{ 500 + (i + 5) % 6 }}</onleft>
    <onright>{{ 500 + (i + 1) % 6 }}</onright>
    <onup>507</onup>
    <ondown>506</ondown>
</control>
<control type="image">
    <posx>{{ 377 + i * 210 }}</posx>
    <posy>{{ vscale(422) }}</posy>
    <width>110</width>
    <height>{{ vscale(110) }}</height>
    <aspectratio>keep</aspectratio>
    <texture>script.plex/reactions/{{ kind }}.png</texture>
</control>
<control type="label">
    <posx>{{ 360 + i * 210 }}</posx>
    <posy>{{ vscale(590) }}</posy>
    <width>180</width>
    <height>{{ vscale(40) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <label>$INFO[Window.Property(label.{{ kind.upper() }})]</label>
</control>
<control type="image">
    <visible>!String.IsEmpty(Window.Property(selected.{{ kind.upper() }}))</visible>
    <posx>{{ 337 + i * 210 }}</posx>
    <posy>{{ vscale(392) }}</posy>
    <width>191</width>
    <height>{{ vscale(191) }}</height>
    <texture border="12" colordiffuse="FFE5A00D">script.plex/white-outline-rounded.png</texture>
</control>
{% endfor %}
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
