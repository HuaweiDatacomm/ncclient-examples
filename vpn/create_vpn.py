##
# Copyright: Copyright (c) Huawei Technologies Co., Ltd. 2021-2021. All rights reserved.
# Description: create a vpn tunnel between PE1 and PE2 using netconf
# Create: 2021-09-22
##

import sys
import logging
from ncclient import manager
from ncclient import operations
from ncclient import xml_

log = logging.getLogger(__name__)

# Configuration
CREATE_VPN_INSTANCE = '''<edit-config>
    <target>
      <candidate/>
    </target>
    <default-operation>none</default-operation>
    <test-option>set</test-option>
    <error-option>rollback-on-error</error-option>
    <config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <dhcp xmlns="urn:huawei:yang:huawei-dhcp">
        <relay>
          <global nc:operation="merge">
            <user-detect-interval>20</user-detect-interval>
            <user-autosave-flag>false</user-autosave-flag>
            <user-store-interval>300</user-store-interval>
            <distribute-flag>false</distribute-flag>
            <opt82-inner-vlan-insert-flag>false</opt82-inner-vlan-insert-flag>
          </global>
        </relay>
      </dhcp>
      <network-instance xmlns="urn:huawei:yang:huawei-network-instance">
        <instances>
          <instance nc:operation="create">
            <name>vrf_ncc_oc_nat</name>
            <afs xmlns="urn:huawei:yang:huawei-l3vpn">
              <af nc:operation="create">
                <type>ipv4-unicast</type>
                <route-distinguisher>3215:4091</route-distinguisher>
                <label-mode>per-route</label-mode>
                <vpn-targets>
                  <vpn-target nc:operation="create">
                    <value>3215:4091</value>
                    <type>export-extcommunity</type>
                  </vpn-target>
                  <vpn-target nc:operation="create">
                    <value>3215:4091</value>
                    <type>import-extcommunity</type>
                  </vpn-target>
                </vpn-targets>
                <routing xmlns="urn:huawei:yang:huawei-routing">
                  <routing-manage>
                    <option nc:operation="create">
                      <frr-enable>false</frr-enable>
                    </option>
                    <topologys>
                      <topology nc:operation="create">
                        <name>base</name>
                      </topology>
                    </topologys>
                  </routing-manage>
                </routing>
                <vpn-ttlmode xmlns="urn:huawei:yang:huawei-mpls-forward" nc:operation="merge">
                  <ttlmode>pipe</ttlmode>
                </vpn-ttlmode>
              </af>
              <af nc:operation="create">
                <type>ipv6-unicast</type>
                <route-distinguisher>3215:4091</route-distinguisher>
                <label-mode>per-route</label-mode>
                <vpn-targets>
                  <vpn-target nc:operation="create">
                    <value>3215:4091</value>
                    <type>export-extcommunity</type>
                  </vpn-target>
                  <vpn-target nc:operation="create">
                    <value>3215:4091</value>
                    <type>import-extcommunity</type>
                  </vpn-target>
                </vpn-targets>
                <routing xmlns="urn:huawei:yang:huawei-routing">
                  <routing-manage>
                    <option nc:operation="create">
                      <frr-enable>false</frr-enable>
                    </option>
                    <topologys>
                      <topology nc:operation="create">
                        <name>base</name>
                      </topology>
                    </topologys>
                  </routing-manage>
                </routing>
                <vpn-ttlmode xmlns="urn:huawei:yang:huawei-mpls-forward" nc:operation="merge">
                  <ttlmode>pipe</ttlmode>
                </vpn-ttlmode>
              </af>
            </afs>
          </instance>
        </instances>
      </network-instance>
    </config>
  </edit-config>'''

CONFIGURE_INTERFACE='''<edit-config>
    <target>
      <candidate/>
    </target>
    <default-operation>none</default-operation>
    <test-option>set</test-option>
    <error-option>rollback-on-error</error-option>
    <config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <dhcp xmlns="urn:huawei:yang:huawei-dhcp">
        <relay>
          <global nc:operation="merge">
            <user-detect-interval>20</user-detect-interval>
            <user-autosave-flag>false</user-autosave-flag>
            <user-store-interval>300</user-store-interval>
            <distribute-flag>false</distribute-flag>
            <opt82-inner-vlan-insert-flag>false</opt82-inner-vlan-insert-flag>
          </global>
        </relay>
      </dhcp>
      <ifm xmlns="urn:huawei:yang:huawei-ifm">
        <interfaces>
          <interface nc:operation="create">
            <name>GigabitEthernet0/3/8.4091</name>
            <class>sub-interface</class>
            <type>GigabitEthernet</type>
            <parent-name>GigabitEthernet0/3/8</parent-name>
            <number>4091</number>
            <description>OC Customer Access</description>
            <admin-status>up</admin-status>
            <link-protocol>ethernet</link-protocol>
            <router-type>broadcast</router-type>
            <statistic-enable>false</statistic-enable>
            <vrf-name>vrf_ncc_oc_nat</vrf-name>
            <ipv4 xmlns="urn:huawei:yang:huawei-ip">
              <addresses>
                <address nc:operation="create">
                  <ip>192.168.51.1</ip>
                  <mask>255.255.255.252</mask>
                  <type>main</type>
                </address>
              </addresses>
            </ipv4>
            <ipv6 xmlns="urn:huawei:yang:huawei-ip" nc:operation="create">
              <spread-mtu-flag>false</spread-mtu-flag>
              <auto-link-local>false</auto-link-local>
              <addresses>
                <address nc:operation="create">
                  <ip>2A01:C000:83:B000:10:20:51:0</ip>
                  <prefix-length>127</prefix-length>
                  <type>global</type>
                </address>
              </addresses>
              <nd-collection xmlns="urn:huawei:yang:huawei-ipv6-nd">
                <if-property nc:operation="create">
                  <retrans-timer>1000</retrans-timer>
                  <nud-reach-time>1200000</nud-reach-time>
                  <attempts-value>1</attempts-value>
                  <max-dyn-nb-num>0</max-dyn-nb-num>
                  <nud-attempts>3</nud-attempts>
                  <na-glean>off</na-glean>
                  <ma-flag>off</ma-flag>
                  <o-flag>off</o-flag>
                  <ra-halt-flag>on</ra-halt-flag>
                  <max-interval>600</max-interval>
                  <ra-preference>medium</ra-preference>
                  <ra-prefix-flag>on</ra-prefix-flag>
                  <ra-mtu-flag>on</ra-mtu-flag>
                  <strict-flag>false</strict-flag>
                  <ts-fuzz-factor>1</ts-fuzz-factor>
                  <ts-clock-drift>1</ts-clock-drift>
                  <ts-delta>300</ts-delta>
                  <rsa-min-key-len>512</rsa-min-key-len>
                  <rsa-max-key-len>2048</rsa-max-key-len>
                  <nud-interval>5000</nud-interval>
                </if-property>
                <proxys nc:operation="create">
                  <route-proxy>off</route-proxy>
                  <inner-vlan-proxy>off</inner-vlan-proxy>
                  <inter-vlan-proxy>off</inter-vlan-proxy>
                  <anyway-proxy>off</anyway-proxy>
                </proxys>
                <ra-property>
                  <ra-control nc:operation="create">
                    <unicast-send>off</unicast-send>
                  </ra-control>
                </ra-property>
              </nd-collection>
            </ipv6>
            <ethernet xmlns="urn:huawei:yang:huawei-ethernet">
              <l3-sub-interface>
                <vlan-type-dot1q nc:operation="create">
                  <vlan-type-vid>4091</vlan-type-vid>
                </vlan-type-dot1q>
              </l3-sub-interface>
            </ethernet>
            <multicast-bas xmlns="urn:huawei:yang:huawei-multicast-bas" nc:operation="create">
              <authorization-enable>false</authorization-enable>
            </multicast-bas>
          </interface>
        </interfaces>
      </ifm>
      <network-instance xmlns="urn:huawei:yang:huawei-network-instance">
        <instances>
          <instance nc:operation="merge">
            <name>vrf_ncc_oc_nat</name>
            <traffic-statistic-enable xmlns="urn:huawei:yang:huawei-l3vpn">false</traffic-statistic-enable>
            <description nc:operation="remove"/>
          </instance>
        </instances>
      </network-instance>
    </config>
  </edit-config>'''

CREATE_ROUTE_POLICY='''<edit-config>
    <target>
      <candidate/>
    </target>
    <default-operation>none</default-operation>
    <test-option>set</test-option>
    <error-option>rollback-on-error</error-option>
    <config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <dhcp xmlns="urn:huawei:yang:huawei-dhcp">
        <relay>
          <global nc:operation="merge">
            <user-detect-interval>20</user-detect-interval>
            <user-autosave-flag>false</user-autosave-flag>
            <user-store-interval>300</user-store-interval>
            <distribute-flag>false</distribute-flag>
            <opt82-inner-vlan-insert-flag>false</opt82-inner-vlan-insert-flag>
          </global>
        </relay>
      </dhcp>
      <routing-policy xmlns="urn:huawei:yang:huawei-routing-policy">
        <policy-definitions>
          <policy-definition nc:operation="create">
            <name>GEN-POL-OUT-VPN-LOCAL-TO-EBGP</name>
            <nodes>
              <node nc:operation="create">
                <sequence>9</sequence>
                <match-mode>permit</match-mode>
                <next-node-choice nc:operation="create">
                  <is-goto-next-node>false</is-goto-next-node>
                </next-node-choice>
              </node>
            </nodes>
          </policy-definition>
          <policy-definition nc:operation="create">
            <name>VPN-STATIC-TO-MPBGP-TEST</name>
            <nodes>
              <node nc:operation="create">
                <sequence>7</sequence>
                <match-mode>permit</match-mode>
                <next-node-choice nc:operation="create">
                  <is-goto-next-node>false</is-goto-next-node>
                </next-node-choice>
              </node>
              <node nc:operation="create">
                <sequence>8</sequence>
                <match-mode>permit</match-mode>
                <next-node-choice nc:operation="create">
                  <is-goto-next-node>false</is-goto-next-node>
                </next-node-choice>
              </node>
            </nodes>
          </policy-definition>
          <policy-definition nc:operation="create">
            <name>GEN-POL-OUT-VPN-STATIC-TO-MPBGP</name>
            <nodes>
              <node nc:operation="create">
                <sequence>6</sequence>
                <match-mode>permit</match-mode>
                <next-node-choice nc:operation="create">
                  <is-goto-next-node>false</is-goto-next-node>
                </next-node-choice>
              </node>
            </nodes>
          </policy-definition>
        </policy-definitions>
      </routing-policy>
    </config>
  </edit-config>'''

CONFIGURE_IPV4_FAMILY='''<edit-config>
    <target>
      <candidate/>
    </target>
    <default-operation>none</default-operation>
    <test-option>set</test-option>
    <error-option>rollback-on-error</error-option>
    <config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <dhcp xmlns="urn:huawei:yang:huawei-dhcp">
        <relay>
          <global nc:operation="merge">
            <user-detect-interval>20</user-detect-interval>
            <user-autosave-flag>false</user-autosave-flag>
            <user-store-interval>300</user-store-interval>
            <distribute-flag>false</distribute-flag>
            <opt82-inner-vlan-insert-flag>false</opt82-inner-vlan-insert-flag>
          </global>
        </relay>
      </dhcp>
      <network-instance xmlns="urn:huawei:yang:huawei-network-instance">
        <instances>
          <instance>
            <name>_public_</name>
            <bgp xmlns="urn:huawei:yang:huawei-bgp">
              <base-process>
                <afs>
                  <af nc:operation="merge">
                    <type>ipv4vpn</type>
                    <ipv4-vpn nc:operation="merge">
                      <policy-vpntarget>false</policy-vpntarget>
                      <reflect-change-path>false</reflect-change-path>
                      <auto-frr>false</auto-frr>
                      <route-select-delay>0</route-select-delay>
                      <apply-label-mode>per-route</apply-label-mode>
                      <nexthop-select-depend-type>depend-ip</nexthop-select-depend-type>
                      <default-med>0</default-med>
                      <best-external>false</best-external>
                      <label-free-delay>0</label-free-delay>
                      <default-local-preference>100</default-local-preference>
                      <bestroute-med-plus-igp>false</bestroute-med-plus-igp>
                      <bestroute-igp-metric-ignore>false</bestroute-igp-metric-ignore>
                      <bestroute-router-id-prior-clusterlist>false</bestroute-router-id-prior-clusterlist>
                      <reflect-between-client>true</reflect-between-client>
                      <activate-route-tag>false</activate-route-tag>
                      <load-balancing-eibgp-enable>false</load-balancing-eibgp-enable>
                      <load-balanc-igp-metric-ignore>false</load-balanc-igp-metric-ignore>
                      <load-balanc-as-path-ignore>false</load-balanc-as-path-ignore>
                      <load-balanc-as-path-relax>false</load-balanc-as-path-relax>
                      <reflector-cluster-ipv4 nc:operation="remove"/>
                      <reflector-cluster-id nc:operation="remove"/>
                      <tunnel-selector-name nc:operation="remove"/>
                      <add-path-select-num nc:operation="remove"/>
                      <route-reflector-ext-community-filter nc:operation="remove"/>
                      <nexthop-recursive-lookup>
                        <common nc:operation="merge">
                          <restrain>true</restrain>
                          <default-route>false</default-route>
                          <route-policy nc:operation="remove"/>
                          <filter-name nc:operation="remove"/>
                        </common>
                        <bit-error-detection nc:operation="merge">
                          <enable>false</enable>
                          <route-policy nc:operation="remove"/>
                          <filter-name nc:operation="remove"/>
                          <filter-parameter nc:operation="remove"/>
                        </bit-error-detection>
                      </nexthop-recursive-lookup>
                      <slow-peer nc:operation="merge">
                        <detection>true</detection>
                        <detection-threshold>300</detection-threshold>
                        <absolute-detection>true</absolute-detection>
                        <absolute-detection-threshold>9</absolute-detection-threshold>
                      </slow-peer>
                    </ipv4-vpn>
                  </af>
                </afs>
                <peers>
                  <peer>
                    <address>5.5.5.5</address>
                    <afs>
                      <af nc:operation="create">
                        <type>ipv4vpn</type>
                        <ipv4-vpn nc:operation="create">
                          <route-update-interval>15</route-update-interval>
                          <public-as-only nc:operation="create">
                            <enable>false</enable>
                          </public-as-only>
                          <public-as-only-import nc:operation="create">
                            <enable>default</enable>
                          </public-as-only-import>
                        </ipv4-vpn>
                      </af>
                    </afs>
                  </peer>
                </peers>
              </base-process>
            </bgp>
          </instance>
          <instance>
            <name>vrf_ncc_oc_nat</name>
            <afs xmlns="urn:huawei:yang:huawei-l3vpn">
              <af>
                <type>ipv4-unicast</type>
                <vpn-ttlmode xmlns="urn:huawei:yang:huawei-mpls-forward" nc:operation="merge">
                  <ttlmode>pipe</ttlmode>
                </vpn-ttlmode>
              </af>
            </afs>
            <bgp xmlns="urn:huawei:yang:huawei-bgp">
              <base-process>
                <afs>
                  <af nc:operation="create">
                    <type>ipv4uni</type>
                    <ipv4-unicast>
                      <common nc:operation="create">
                        <auto-frr>false</auto-frr>
                        <maximum-load-balancing-ibgp>1</maximum-load-balancing-ibgp>
                        <maximum-load-balancing-ebgp>1</maximum-load-balancing-ebgp>
                        <nexthop-resolve-aigp>false</nexthop-resolve-aigp>
                        <summary-automatic>false</summary-automatic>
                        <best-route-bit-error-detection>false</best-route-bit-error-detection>
                        <supernet-unicast-advertise>false</supernet-unicast-advertise>
                        <supernet-label-advertise>true</supernet-label-advertise>
                        <lsp-mtu>1500</lsp-mtu>
                        <label-free-delay>0</label-free-delay>
                        <bestroute-as-path-ignore>false</bestroute-as-path-ignore>
                        <determin-med>false</determin-med>
                        <attribute-set-enable>false</attribute-set-enable>
                        <load-balanc-igp-metric-ignore>false</load-balanc-igp-metric-ignore>
                        <load-balanc-as-path-ignore>false</load-balanc-as-path-ignore>
                        <load-balanc-as-path-relax>false</load-balanc-as-path-relax>
                        <maximum-load-balancing>1</maximum-load-balancing>
                        <import-rib-nexthop-invariable>false</import-rib-nexthop-invariable>
                        <route-relay-tunnel>false</route-relay-tunnel>
                        <bestroute-med-plus-igp>false</bestroute-med-plus-igp>
                        <bestroute-igp-metric-ignore>false</bestroute-igp-metric-ignore>
                        <bestroute-router-id-prior-clusterlist>false</bestroute-router-id-prior-clusterlist>
                        <bestroute-med-none-as-maximum>false</bestroute-med-none-as-maximum>
                        <load-balancing-eibgp-enable>false</load-balancing-eibgp-enable>
                        <prefix-origin-as-validation>false</prefix-origin-as-validation>
                        <advertise-route-mode>all</advertise-route-mode>
                        <reoriginate-route>false</reoriginate-route>
                        <route-select-delay>0</route-select-delay>
                        <reflect-change-path>false</reflect-change-path>
                        <always-compare-med>false</always-compare-med>
                        <default-med>0</default-med>
                        <nexthop-third-party>false</nexthop-third-party>
                        <default-local-preference>100</default-local-preference>
                        <default-route-import>false</default-route-import>
                        <routerid-neglect>false</routerid-neglect>
                        <reflect-between-client>true</reflect-between-client>
                        <ext-community-change>false</ext-community-change>
                        <active-route-advertise>false</active-route-advertise>
                        <ebgp-interface-sensitive>true</ebgp-interface-sensitive>
                      </common>
                      <preference nc:operation="create">
                        <external>255</external>
                        <internal>255</internal>
                        <local>255</local>
                      </preference>
                      <nexthop-recursive-lookup>
                        <common nc:operation="create">
                          <restrain>true</restrain>
                          <default-route>false</default-route>
                        </common>
                      </nexthop-recursive-lookup>
                      <import-routes>
                        <import-route nc:operation="create">
                          <protocol>direct</protocol>
                          <process-id>0</process-id>
                        </import-route>
                        <import-route nc:operation="create">
                          <protocol>static</protocol>
                          <process-id>0</process-id>
                          <policy-name>GEN-POL-OUT-VPN-STATIC-TO-MPBGP</policy-name>
                        </import-route>
                      </import-routes>
                      <lsp-options nc:operation="create">
                        <ingress-protect-mode-bgp-frr>false</ingress-protect-mode-bgp-frr>
                        <maximum-load-balancing-ingress>1</maximum-load-balancing-ingress>
                        <maximum-load-balancing-transit>1</maximum-load-balancing-transit>
                      </lsp-options>
                      <slow-peer nc:operation="create">
                        <detection>true</detection>
                        <detection-threshold>300</detection-threshold>
                        <absolute-detection>true</absolute-detection>
                        <absolute-detection-threshold>9</absolute-detection-threshold>
                      </slow-peer>
                      <routing-table-rib-only nc:operation="create">
                        <enable>false</enable>
                      </routing-table-rib-only>
                    </ipv4-unicast>
                  </af>
                </afs>
                <peers>
                  <peer nc:operation="create">
                    <address>30.0.0.1</address>
                    <remote-as>65001</remote-as>
                    <ebgp-max-hop>1</ebgp-max-hop>
                    <local-ifnet-disable>false</local-ifnet-disable>
                    <timer nc:operation="create">
                      <keep-alive-time>60</keep-alive-time>
                      <hold-time>180</hold-time>
                      <min-hold-time>0</min-hold-time>
                      <connect-retry-time>32</connect-retry-time>
                    </timer>
                    <graceful-restart nc:operation="create">
                      <enable>default</enable>
                      <peer-reset>default</peer-reset>
                    </graceful-restart>
                    <local-graceful-restart nc:operation="create">
                      <enable>default</enable>
                    </local-graceful-restart>
                    <afs>
                      <af nc:operation="create">
                        <type>ipv4uni</type>
                        <ipv4-unicast nc:operation="create">
                          <import-policy>GEN-POL-OUT-VPN-LOCAL-TO-EBGP</import-policy>
                          <export-policy>GEN-POL-OUT-VPN-LOCAL-TO-EBGP</export-policy>
                          <route-update-interval>30</route-update-interval>
                          <public-as-only nc:operation="create">
                            <enable>false</enable>
                          </public-as-only>
                          <public-as-only-import nc:operation="create">
                            <enable>default</enable>
                          </public-as-only-import>
                        </ipv4-unicast>
                      </af>
                    </afs>
                  </peer>
                </peers>
              </base-process>
            </bgp>
          </instance>
        </instances>
      </network-instance>
    </config>
  </edit-config>'''

CONFIGURE_IPV6_FAMILY='''<edit-config>
    <target>
      <candidate/>
    </target>
    <default-operation>none</default-operation>
    <test-option>set</test-option>
    <error-option>rollback-on-error</error-option>
    <config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <dhcp xmlns="urn:huawei:yang:huawei-dhcp">
        <relay>
          <global nc:operation="merge">
            <user-detect-interval>20</user-detect-interval>
            <user-autosave-flag>false</user-autosave-flag>
            <user-store-interval>300</user-store-interval>
            <distribute-flag>false</distribute-flag>
            <opt82-inner-vlan-insert-flag>false</opt82-inner-vlan-insert-flag>
          </global>
        </relay>
      </dhcp>
      <network-instance xmlns="urn:huawei:yang:huawei-network-instance">
        <instances>
          <instance>
            <name>_public_</name>
            <bgp xmlns="urn:huawei:yang:huawei-bgp">
              <base-process>
                <peers>
                  <peer>
                    <address>5.5.5.5</address>
                    <afs>
                      <af nc:operation="create">
                        <type>ipv6vpn</type>
                        <ipv6-vpn nc:operation="create">
                          <route-update-interval>15</route-update-interval>
                          <public-as-only nc:operation="create">
                            <enable>false</enable>
                          </public-as-only>
                          <public-as-only-import nc:operation="create">
                            <enable>default</enable>
                          </public-as-only-import>
                        </ipv6-vpn>
                      </af>
                    </afs>
                  </peer>
                </peers>
              </base-process>
            </bgp>
          </instance>
          <instance>
            <name>vrf_ncc_oc_nat</name>
            <afs xmlns="urn:huawei:yang:huawei-l3vpn">
              <af>
                <type>ipv6-unicast</type>
                <vpn-ttlmode xmlns="urn:huawei:yang:huawei-mpls-forward" nc:operation="merge">
                  <ttlmode>pipe</ttlmode>
                </vpn-ttlmode>
              </af>
            </afs>
            <bgp xmlns="urn:huawei:yang:huawei-bgp">
              <base-process>
                <afs>
                  <af nc:operation="create">
                    <type>ipv6uni</type>
                    <ipv6-unicast>
                      <common nc:operation="create">
                        <router-id-auto-select>false</router-id-auto-select>
                        <auto-frr>false</auto-frr>
                        <maximum-load-balancing-ibgp>1</maximum-load-balancing-ibgp>
                        <maximum-load-balancing-ebgp>1</maximum-load-balancing-ebgp>
                        <nexthop-resolve-aigp>false</nexthop-resolve-aigp>
                        <supernet-unicast-advertise>false</supernet-unicast-advertise>
                        <bestroute-as-path-ignore>false</bestroute-as-path-ignore>
                        <determin-med>false</determin-med>
                        <attribute-set-enable>false</attribute-set-enable>
                        <load-balanc-igp-metric-ignore>false</load-balanc-igp-metric-ignore>
                        <load-balanc-as-path-ignore>false</load-balanc-as-path-ignore>
                        <load-balanc-as-path-relax>false</load-balanc-as-path-relax>
                        <maximum-load-balancing>1</maximum-load-balancing>
                        <best-route-bit-error-detection>false</best-route-bit-error-detection>
                        <import-rib-nexthop-invariable>false</import-rib-nexthop-invariable>
                        <route-relay-tunnel-v4>false</route-relay-tunnel-v4>
                        <bestroute-med-plus-igp>false</bestroute-med-plus-igp>
                        <bestroute-igp-metric-ignore>false</bestroute-igp-metric-ignore>
                        <bestroute-router-id-prior-clusterlist>false</bestroute-router-id-prior-clusterlist>
                        <bestroute-med-none-as-maximum>false</bestroute-med-none-as-maximum>
                        <load-balancing-eibgp-enable>false</load-balancing-eibgp-enable>
                        <prefix-origin-as-validation>false</prefix-origin-as-validation>
                        <advertise-route-mode>all</advertise-route-mode>
                        <route-select-delay>0</route-select-delay>
                        <reflect-change-path>false</reflect-change-path>
                        <always-compare-med>false</always-compare-med>
                        <default-med>0</default-med>
                        <nexthop-third-party>false</nexthop-third-party>
                        <default-local-preference>100</default-local-preference>
                        <default-route-import>false</default-route-import>
                        <routerid-neglect>false</routerid-neglect>
                        <reflect-between-client>true</reflect-between-client>
                        <ext-community-change>false</ext-community-change>
                        <active-route-advertise>false</active-route-advertise>
                        <ebgp-interface-sensitive>true</ebgp-interface-sensitive>
                      </common>
                      <preference nc:operation="create">
                        <external>255</external>
                        <internal>255</internal>
                        <local>255</local>
                      </preference>
                      <nexthop-recursive-lookup>
                        <common nc:operation="create">
                          <restrain>true</restrain>
                          <default-route>false</default-route>
                        </common>
                      </nexthop-recursive-lookup>
                      <import-routes>
                        <import-route nc:operation="create">
                          <protocol>direct</protocol>
                          <process-id>0</process-id>
                        </import-route>
                        <import-route nc:operation="create">
                          <protocol>static</protocol>
                          <process-id>0</process-id>
                          <policy-name>GEN-POL-OUT-VPN-STATIC-TO-MPBGP</policy-name>
                        </import-route>
                      </import-routes>
                      <slow-peer nc:operation="create">
                        <detection>true</detection>
                        <detection-threshold>300</detection-threshold>
                        <absolute-detection>true</absolute-detection>
                        <absolute-detection-threshold>9</absolute-detection-threshold>
                      </slow-peer>
                      <routing-table-rib-only nc:operation="create">
                        <enable>false</enable>
                      </routing-table-rib-only>
                      <qos nc:operation="create">
                        <ipv6-qppb>false</ipv6-qppb>
                      </qos>
                    </ipv6-unicast>
                  </af>
                </afs>
                <peers>
                  <peer nc:operation="create">
                    <address>30::1</address>
                    <remote-as>65001</remote-as>
                    <ebgp-max-hop>1</ebgp-max-hop>
                    <timer nc:operation="create">
                      <keep-alive-time>60</keep-alive-time>
                      <hold-time>180</hold-time>
                      <min-hold-time>0</min-hold-time>
                      <connect-retry-time>32</connect-retry-time>
                    </timer>
                    <graceful-restart nc:operation="create">
                      <enable>default</enable>
                      <peer-reset>default</peer-reset>
                    </graceful-restart>
                    <local-graceful-restart nc:operation="create">
                      <enable>default</enable>
                    </local-graceful-restart>
                    <afs>
                      <af nc:operation="create">
                        <type>ipv6uni</type>
                        <ipv6-unicast nc:operation="create">
                          <import-policy>GEN-POL-OUT-VPN-LOCAL-TO-EBGP</import-policy>
                          <export-policy>GEN-POL-OUT-VPN-LOCAL-TO-EBGP</export-policy>
                          <route-update-interval>30</route-update-interval>
                          <public-as-only nc:operation="create">
                            <enable>false</enable>
                          </public-as-only>
                          <public-as-only-import nc:operation="create">
                            <enable>default</enable>
                          </public-as-only-import>
                        </ipv6-unicast>
                      </af>
                    </afs>
                  </peer>
                </peers>
              </base-process>
            </bgp>
          </instance>
        </instances>
      </network-instance>
    </config>
  </edit-config>'''

CONFIGURE_STATIC_ROUTE_IPV4='''<edit-config>
    <target>
      <candidate/>
    </target>
    <default-operation>none</default-operation>
    <test-option>set</test-option>
    <error-option>rollback-on-error</error-option>
    <config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <dhcp xmlns="urn:huawei:yang:huawei-dhcp">
        <relay>
          <global nc:operation="merge">
            <user-detect-interval>20</user-detect-interval>
            <user-autosave-flag>false</user-autosave-flag>
            <user-store-interval>300</user-store-interval>
            <distribute-flag>false</distribute-flag>
            <opt82-inner-vlan-insert-flag>false</opt82-inner-vlan-insert-flag>
          </global>
        </relay>
      </dhcp>
      <network-instance xmlns="urn:huawei:yang:huawei-network-instance">
        <instances>
          <instance>
            <name>vrf_ncc_oc_nat</name>
            <afs xmlns="urn:huawei:yang:huawei-l3vpn">
              <af>
                <type>ipv4-unicast</type>
                <routing xmlns="urn:huawei:yang:huawei-routing">
                  <static-routing>
                    <unicast-route2s>
                      <unicast-route2 nc:operation="create">
                        <topology-name>base</topology-name>
                        <prefix>51.1.1.0</prefix>
                        <mask-length>24</mask-length>
                        <nexthop-addresses>
                          <nexthop-address nc:operation="create">
                            <address>192.168.51.2</address>
                            <preference>60</preference>
                            <tag>110</tag>
                          </nexthop-address>
                        </nexthop-addresses>
                      </unicast-route2>
                    </unicast-route2s>
                  </static-routing>
                </routing>
                <vpn-ttlmode xmlns="urn:huawei:yang:huawei-mpls-forward" nc:operation="merge">
                  <ttlmode>pipe</ttlmode>
                </vpn-ttlmode>
              </af>
              <af>
                <type>ipv6-unicast</type>
                <vpn-ttlmode xmlns="urn:huawei:yang:huawei-mpls-forward" nc:operation="merge">
                  <ttlmode>pipe</ttlmode>
                </vpn-ttlmode>
              </af>
            </afs>
          </instance>
        </instances>
      </network-instance>
      <routing xmlns="urn:huawei:yang:huawei-routing">
        <static-routing>
          <ipv4-site nc:operation="merge">
            <preference>60</preference>
            <relay-switch>false</relay-switch>
            <min-tx-interval>50</min-tx-interval>
            <min-rx-interval>50</min-rx-interval>
            <multiplier>3</multiplier>
            <relay-remote>true</relay-remote>
            <relay-arp-vlink>false</relay-arp-vlink>
            <inherit-cost-switch>false</inherit-cost-switch>
            <relay-srv6-nexthop>false</relay-srv6-nexthop>
          </ipv4-site>
          <ipv4-relay-tunnel nc:operation="merge">
            <enable>false</enable>
          </ipv4-relay-tunnel>
          <ipv6-site nc:operation="merge">
            <preference>60</preference>
            <min-tx-interval>50</min-tx-interval>
            <min-rx-interval>50</min-rx-interval>
            <multiplier>3</multiplier>
            <relay-arp-vlink6>false</relay-arp-vlink6>
            <relay-srv6-nexthop6>false</relay-srv6-nexthop6>
          </ipv6-site>
        </static-routing>
      </routing>
    </config>
  </edit-config>'''

CONFIGURE_STATIC_ROUTE_IPV6='''<edit-config>
    <target>
      <candidate/>
    </target>
    <default-operation>none</default-operation>
    <test-option>set</test-option>
    <error-option>rollback-on-error</error-option>
    <config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <dhcp xmlns="urn:huawei:yang:huawei-dhcp">
        <relay>
          <global nc:operation="merge">
            <user-detect-interval>20</user-detect-interval>
            <user-autosave-flag>false</user-autosave-flag>
            <user-store-interval>300</user-store-interval>
            <distribute-flag>false</distribute-flag>
            <opt82-inner-vlan-insert-flag>false</opt82-inner-vlan-insert-flag>
          </global>
        </relay>
      </dhcp>
      <network-instance xmlns="urn:huawei:yang:huawei-network-instance">
        <instances>
          <instance>
            <name>vrf_ncc_oc_nat</name>
            <afs xmlns="urn:huawei:yang:huawei-l3vpn">
              <af>
                <type>ipv4-unicast</type>
                <vpn-ttlmode xmlns="urn:huawei:yang:huawei-mpls-forward" nc:operation="merge">
                  <ttlmode>pipe</ttlmode>
                </vpn-ttlmode>
              </af>
              <af>
                <type>ipv6-unicast</type>
                <routing xmlns="urn:huawei:yang:huawei-routing">
                  <static-routing>
                    <unicast-route2s>
                      <unicast-route2 nc:operation="create">
                        <topology-name>base</topology-name>
                        <prefix>AA:51::</prefix>
                        <mask-length>64</mask-length>
                        <nexthop-addresses>
                          <nexthop-address nc:operation="create">
                            <address>2A01:C000:83:B000:10:20:51:1</address>
                            <preference>60</preference>
                            <tag>181</tag>
                          </nexthop-address>
                        </nexthop-addresses>
                      </unicast-route2>
                    </unicast-route2s>
                  </static-routing>
                </routing>
                <vpn-ttlmode xmlns="urn:huawei:yang:huawei-mpls-forward" nc:operation="merge">
                  <ttlmode>pipe</ttlmode>
                </vpn-ttlmode>
              </af>
            </afs>
          </instance>
        </instances>
      </network-instance>
      <routing xmlns="urn:huawei:yang:huawei-routing">
        <static-routing>
          <ipv4-site nc:operation="merge">
            <preference>60</preference>
            <relay-switch>false</relay-switch>
            <min-tx-interval>50</min-tx-interval>
            <min-rx-interval>50</min-rx-interval>
            <multiplier>3</multiplier>
            <relay-remote>true</relay-remote>
            <relay-arp-vlink>false</relay-arp-vlink>
            <inherit-cost-switch>false</inherit-cost-switch>
            <relay-srv6-nexthop>false</relay-srv6-nexthop>
          </ipv4-site>
          <ipv4-relay-tunnel nc:operation="merge">
            <enable>false</enable>
          </ipv4-relay-tunnel>
          <ipv6-site nc:operation="merge">
            <preference>60</preference>
            <min-tx-interval>50</min-tx-interval>
            <min-rx-interval>50</min-rx-interval>
            <multiplier>3</multiplier>
            <relay-arp-vlink6>false</relay-arp-vlink6>
            <relay-srv6-nexthop6>false</relay-srv6-nexthop6>
          </ipv6-site>
        </static-routing>
      </routing>
    </config>
  </edit-config>'''

# Fill the device information and establish a NETCONF session

def huawei_connect(host, port, user, password):
    return manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           hostkey_verify = False,
                           device_params={'name': "huaweiyang"},
                           allow_agent = False,
                           look_for_keys = False)

def _check_response(rpc_obj, snippet_name):
    print("Check the edit reply for %s is \n%s" % (snippet_name, rpc_obj.xml))
    xml_str = rpc_obj.xml
    if "<ok/>" in xml_str:
        print("Execute successfully.\n")
        return True
    else:
        print("Execute unccessfully\n.")
        return False

def send_editconfig_rpc(m, rpc):
    print("Step 2: Send <edit_config> rpc in candidate and check reply.\n")
    rpc_obj = m.dispatch(xml_.to_ele(rpc))
    # m.edit_config(target='candidate', config=rpc)
    ckResult = _check_response(rpc_obj, 'CREATE_VPN')

    if ckResult:
        print("Step 3: Send commit rpc and check reply.\n")
        cmtObj = m.commit()
        print("Get the commit reply\n%s"% cmtObj.xml)

def create_vpn_instance(host, port, user, password):
    print("Step 1: Establish a netconf connection.\n")
    with huawei_connect(host, port=port, user=user, password=password) as m:
        print("This netconf session ID = %s.\n"% (m._session.id))

        # create vpn instance
        print("(1) create a vpn instance")
        send_editconfig_rpc(m, CREATE_VPN_INSTANCE)
        # configure a interface
        print("(2) configure a interface")
        send_editconfig_rpc(m, CONFIGURE_INTERFACE)
        # create route policy
        print("(3) create route policy")
        send_editconfig_rpc(m, CREATE_ROUTE_POLICY)
        # configure ipv4 family
        print("(4) configure ipv4 family")
        send_editconfig_rpc(m, CONFIGURE_IPV4_FAMILY)
        # configure ipv6 family
        print("(5) configure ipv6 family")
        send_editconfig_rpc(m, CONFIGURE_IPV6_FAMILY)
        # configure static route for ipv4
        print("(6) configure static route for ipv4")
        send_editconfig_rpc(m, CONFIGURE_STATIC_ROUTE_IPV4)
        # configure static route for ipv6
        print("(7) configure static route for ipv6")
        send_editconfig_rpc(m, CONFIGURE_STATIC_ROUTE_IPV6)

if __name__ == '__main__':
    create_vpn_instance(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
