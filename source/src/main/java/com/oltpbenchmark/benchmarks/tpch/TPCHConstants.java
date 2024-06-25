/*
 * Copyright 2020 by OLTPBenchmark Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

package com.oltpbenchmark.benchmarks.tpch;

public class TPCHConstants {

  public static final String TABLENAME_REGION = "region";
  public static final String TABLENAME_NATION = "nation";
  public static final String TABLENAME_SUPPLIER = "supplier";
  public static final String TABLENAME_CUSTOMER = "customer";
  public static final String TABLENAME_PART = "part";
  public static final String TABLENAME_ORDER = "orders";
  public static final String TABLENAME_PARTSUPP = "partsupp";
  public static final String TABLENAME_LINEITEM = "lineitem";

  // 4.2.2.13 CONTAINERS SYLLABLE 1
  public static final String[] CONTAINERS_S1 = {"SM", "LG", "MED", "JUMBO", "WRAP"};

  // 4.2.2.13 CONTAINERS SYLLABLE 2
  public static final String[] CONTAINERS_S2 = {
    "CASE", "BOX", "BAG", "JAR", "PKG", "PACK", "CAN", "DRUM"
  };

  // 4.2.2.13 MODES
  public static final String[] MODES = {"REG AIR", "AIR", "RAIL", "SHIP", "TRUCK", "MAIL", "FOB"};

  // 4.2.2.13 SEGMENTS
  public static final String[] SEGMENTS = {
    "AUTOMOBILE", "BUILDING", "FURNITURE", "MACHINERY", "HOUSEHOLD"
  };

  // 4.2.2.13 TYPE SYLLABLE 1
  public static final String[] TYPE_S1 = {
    "STANDARD", "SMALL", "MEDIUM", "LARGE", "ECONOMY", "PROMO"
  };

  // 4.2.2.13 TYPE SYLLABLE 2
  public static final String[] TYPE_S2 = {"ANODIZED", "BURNISHED", "PLATED", "POLISHED", "BRUSHED"};

  // 4.2.2.13 TYPE SYLLABLE 3
  public static final String[] TYPE_S3 = {"TIN", "NICKEL", "BRASS", "STEEL", "COPPER"};

  // 4.2.3 N_NAME
  public static final String[] N_NAME = {
    "ALGERIA",
    "ARGENTINA",
    "BRAZIL",
    "CANADA",
    "EGYPT",
    "ETHIOPIA",
    "FRANCE",
    "GERMANY",
    "INDIA",
    "INDONESIA",
    "IRAN",
    "IRAQ",
    "JAPAN",
    "JORDAN",
    "KENYA",
    "MOROCCO",
    "MOZAMBIQUE",
    "PERU",
    "CHINA",
    "ROMANIA",
    "SAUDI ARABIA",
    "VIETNAM",
    "RUSSIA",
    "UNITED KINGDOM",
    "UNITED STATES"
  };

  // 4.2.3 P_NAME generated by concatenating five of these
  public static final String[] P_NAME_GENERATOR = {
    "almond",
    "antique",
    "aquamarine",
    "azure",
    "beige",
    "bisque",
    "black",
    "blanched",
    "blue",
    "blush",
    "brown",
    "burlywood",
    "burnished",
    "chartreuse",
    "chiffon",
    "chocolate",
    "coral",
    "cornflower",
    "cornsilk",
    "cream",
    "cyan",
    "dark",
    "deep",
    "dim",
    "dodger",
    "drab",
    "firebrick",
    "floral",
    "forest",
    "frosted",
    "gainsboro",
    "ghost",
    "goldenrod",
    "green",
    "grey",
    "honeydew",
    "hot",
    "indian",
    "ivory",
    "khaki",
    "lace",
    "lavender",
    "lawn",
    "lemon",
    "light",
    "lime",
    "linen",
    "magenta",
    "maroon",
    "medium",
    "metallic",
    "midnight",
    "mint",
    "misty",
    "moccasin",
    "navajo",
    "navy",
    "olive",
    "orange",
    "orchid",
    "pale",
    "papaya",
    "peach",
    "peru",
    "pink",
    "plum",
    "powder",
    "puff",
    "purple",
    "red",
    "rose",
    "rosy",
    "royal",
    "saddle",
    "salmon",
    "sandy",
    "seashell",
    "sienna",
    "sky",
    "slate",
    "smoke",
    "snow",
    "spring",
    "steel",
    "tan",
    "thistle",
    "tomato",
    "turquoise",
    "violet",
    "wheat",
    "white",
    "yellow"
  };

  // 4.2.3 R_NAME
  public static final String[] R_NAME = {"AFRICA", "AMERICA", "ASIA", "EUROPE", "MIDDLE EAST"};
}
