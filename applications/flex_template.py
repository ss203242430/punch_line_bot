def cat_monster_flex_template(hp_percent, description):
    return {
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "nano",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "(^=◕ᴥ◕=^)",
                "color": "#ffffff",
                "align": "center",
                "size": "md",
                "gravity": "center"
              },
              {
                "type": "text",
                "text": "HP: ",
                "color": "#ffffff",
                "align": "start",
                "size": "xs",
                "gravity": "center",
                "margin": "lg"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "filler"
                      }
                    ],
                    "width": f"{hp_percent}%",
                    "backgroundColor": "#FF0000",
                    "height": "6px"
                  }
                ],
                "backgroundColor": "#9FD8E36E",
                "height": "6px",
                "margin": "sm"
              }
            ],
            "backgroundColor": "#27ACB2",
            "paddingTop": "19px",
            "paddingAll": "12px",
            "paddingBottom": "16px"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": description,
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                  }
                ],
                "flex": 1
              }
            ],
            "spacing": "md",
            "paddingAll": "12px"
          },
          "styles": {
            "footer": {
              "separator": False
            }
          }
        }
      ]
    }

def damage_statistics_flex_template():
    return {
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "kilo",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "backgroundColor": "#27ACB2",
            "paddingTop": "5px",
            "paddingAll": "12px",
            "paddingBottom": "16px"
          },
          "styles": {
            "footer": {
              "separator": False
            }
          }
        }
      ]
    }


def npc_info_flex_template(npc_id, item, damage_percentage):
    return {
      "type": "text",
      "text": str(npc_id) + ': ' + item['name'] + ' 造成 ' + str(item['damage']) + ' 傷害，佔 ' + \
        str(damage_percentage) + ' %',
      "color": "#ffffff",
      "align": "start",
      "size": "xs",
      "gravity": "center",
      "margin": "lg"
    }

def damage_bar_graph_flex_template(damage_percentage):
    return {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "filler"
            }
          ],
          "width": f"{damage_percentage}%",
          "backgroundColor": "#0D8186",
          "height": "6px"
        }
      ],
      "backgroundColor": "#9FD8E36E",
      "height": "6px",
      "margin": "sm"
    }

def learn_punch_flex_template(title, description, total_time, clock_in_str, clock_out_str):
    return {
      "type": "bubble",
      "size": "kilo",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "標題",
                "color": "#ffffff66",
                "size": "sm"
              },
              {
                "type": "text",
                "text": title,
                "color": "#ffffff",
                "size": "xl",
                "flex": 4,
                "weight": "bold"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "描述",
                "color": "#ffffff66",
                "size": "sm"
              },
              {
                "type": "text",
                "text": description,
                "color": "#ffffff",
                "size": "md",
                "flex": 4,
                "weight": "bold"
              }
            ]
          }
        ],
        "paddingAll": "20px",
        "backgroundColor": "#0367D3",
        "spacing": "md",
        "height": "154px",
        "paddingTop": "22px"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": f"Total: {total_time}",
            "color": "#b7b7b7",
            "size": "xs"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "開始",
                "size": "sm",
                "gravity": "center"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "cornerRadius": "30px",
                    "height": "12px",
                    "width": "12px",
                    "borderColor": "#EF454D",
                    "borderWidth": "2px"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "flex": 0
              },
              {
                "type": "text",
                "text": clock_in_str,
                "gravity": "center",
                "flex": 4,
                "size": "sm"
              }
            ],
            "spacing": "lg",
            "cornerRadius": "30px",
            "margin": "xl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": "#B7B7B7"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "12px"
              },
              {
                "type": "text",
                "gravity": "center",
                "flex": 4,
                "size": "xs",
                "color": "#8c8c8c",
                "text": " "
              }
            ],
            "spacing": "lg",
            "height": "64px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "結束",
                "gravity": "center",
                "size": "sm"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "cornerRadius": "30px",
                    "width": "12px",
                    "height": "12px",
                    "borderColor": "#6486E3",
                    "borderWidth": "2px"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "flex": 0
              },
              {
                "type": "text",
                "text": clock_out_str,
                "gravity": "center",
                "flex": 4,
                "size": "sm"
              }
            ],
            "spacing": "lg",
            "cornerRadius": "30px"
          }
        ]
      }
    }