{% extends "default.xml.tpl" %}
{% block header %}{% endblock %}
{% block headers %}
<defaultcontrol>401</defaultcontrol>
{% endblock %}
{% block content %}
<control type="label">
    <posx>60</posx>
    <posy>{{ vscale(60) }}</posy>
    <width>1500</width>
    <height>{{ vscale(60) }}</height>
    <font>font13</font>
    <textcolor>FFFFFFFF</textcolor>
    <align>left</align>
    <label>$ADDON[script.plexmod 35130]</label>
</control>
<control type="label">
    <posx>60</posx>
    <posy>{{ vscale(126) }}</posy>
    <width>1700</width>
    <height>{{ vscale(48) }}</height>
    <font>font12</font>
    <textcolor>DDFFFFFF</textcolor>
    <align>left</align>
    <label>$INFO[Window.Property(title)]</label>
</control>
<control type="button" id="301">
    <posx>60</posx>
    <posy>{{ vscale(212) }}</posy>
    <width>180</width>
    <height>{{ vscale(52) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$INFO[Window.Property(sort.TOP)]</label>
    <onleft>307</onleft>
    <onright>302</onright>
    <ondown>401</ondown>
    <onup>152</onup>
</control>
<control type="button" id="302">
    <posx>260</posx>
    <posy>{{ vscale(212) }}</posy>
    <width>180</width>
    <height>{{ vscale(52) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$INFO[Window.Property(sort.RECENT)]</label>
    <onleft>301</onleft>
    <onright>303</onright>
    <ondown>401</ondown>
    <onup>152</onup>
</control>
<control type="button" id="303">
    <posx>460</posx>
    <posy>{{ vscale(212) }}</posy>
    <width>180</width>
    <height>{{ vscale(52) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$INFO[Window.Property(sort.HOT)]</label>
    <onleft>302</onleft>
    <onright>304</onright>
    <ondown>401</ondown>
    <onup>152</onup>
</control>
<control type="button" id="304">
    <posx>660</posx>
    <posy>{{ vscale(212) }}</posy>
    <width>180</width>
    <height>{{ vscale(52) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$INFO[Window.Property(sort.FRIENDS)]</label>
    <onleft>303</onleft>
    <onright>305</onright>
    <ondown>401</ondown>
    <onup>152</onup>
</control>
<control type="button" id="305">
    <posx>1180</posx>
    <posy>{{ vscale(212) }}</posy>
    <width>200</width>
    <height>{{ vscale(52) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$ADDON[script.plexmod 35111]</label>
    <onleft>304</onleft>
    <onright>306</onright>
    <ondown>401</ondown>
    <onup>152</onup>
    <visible>!String.IsEmpty(Window.Property(has.previous))</visible>
</control>
<control type="button" id="306">
    <posx>1400</posx>
    <posy>{{ vscale(212) }}</posy>
    <width>200</width>
    <height>{{ vscale(52) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$ADDON[script.plexmod 35110]</label>
    <onleft>305</onleft>
    <onright>307</onright>
    <ondown>401</ondown>
    <onup>152</onup>
    <visible>!String.IsEmpty(Window.Property(has.next))</visible>
</control>
<control type="button" id="307">
    <posx>1620</posx>
    <posy>{{ vscale(212) }}</posy>
    <width>240</width>
    <height>{{ vscale(52) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <focusedcolor>FF111111</focusedcolor>
    <texturefocus colordiffuse="FFFFFFFF" border="8">script.plex/white-square-rounded.png</texturefocus>
    <texturenofocus colordiffuse="55000000" border="8">script.plex/white-square-rounded.png</texturenofocus>
    <label>$ADDON[script.plexmod 35135]</label>
    <onleft>306</onleft>
    <onright>301</onright>
    <ondown>401</ondown>
    <onup>152</onup>
</control>
<control type="list" id="401">
    <posx>0</posx>
    <posy>{{ vscale(305) }}</posy>
    <width>1920</width>
    <height>{{ vscale(450) }}</height>
    <orientation>horizontal</orientation>
    <onup>301</onup>
    <ondown>306</ondown>
    <scrolltime>200</scrolltime>
    {% include "includes/community_cards.xml.tpl" %}
</control>
<control type="label">
    <posx>60</posx>
    <posy>{{ vscale(780) }}</posy>
    <width>1800</width>
    <height>{{ vscale(70) }}</height>
    <font>font10</font>
    <textcolor>DDFFFFFF</textcolor>
    <align>left</align>
    <label>$INFO[Window.Property(status)]</label>
</control>
{% endblock %}
