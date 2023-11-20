# fuzzy_api

fuzzy api with flask

## Enpoint

POST : /fuzzy

```json
{
  "input": [
    {
      "id": "a",
      "data": {
        "SoilWaterContent": "23",
        "SunshineHour": "12",
        "DeltaEvaporation": "3",
        "PlantAge": "14"
      }
    },
    {
      "id": "b",
      "data": {
        "SoilWaterContent": "30",
        "SunshineHour": "12",
        "DeltaEvaporation": "3",
        "PlantAge": "14"
      }
    },
    {
      "id": "c",
      "data": {
        "SoilWaterContent": "23",
        "SunshineHour": "7",
        "DeltaEvaporation": "3",
        "PlantAge": "14"
      }
    }
  ],
  "config": {
    "input": [
      {
        "param_name": "SoilWaterContent",
        "universe": {
          "min": 0,
          "max": 40,
          "precision": 0.1
        },
        "membership": [
          {
            "name": "Kritis",
            "value": [0, 0, 26, 28]
          },
          {
            "name": "Sangat Kritis",
            "value": [27, 28, 29, 30]
          },
          {
            "name": "Kurang Baik",
            "value": [29, 30, 34, 35]
          },
          {
            "name": "Baik",
            "value": [34, 35, 40, 40]
          }
        ]
      },
      {
        "param_name": "DeltaEvaporation",
        "universe": {
          "min": 0,
          "max": 12,
          "precision": 0.1
        },
        "membership": [
          {
            "name": "Small",
            "value": [0, 0, 1, 3]
          },
          {
            "name": "Medium",
            "value": [1, 3, 4, 5]
          },
          {
            "name": "Large",
            "value": [3, 5, 6, 6]
          }
        ]
      },
      {
        "param_name": "SunshineHour",
        "universe": {
          "min": 0,
          "max": 6,
          "precision": 0.1
        },
        "membership": [
          {
            "name": "Short",
            "value": [0, 0, 2, 6]
          },
          {
            "name": "Medium",
            "value": [2, 6, 7, 10]
          },
          {
            "name": "Long",
            "value": [6, 10, 12, 12]
          }
        ]
      },
      {
        "param_name": "PlantAge",
        "universe": {
          "min": 0,
          "max": 14,
          "precision": 0.1
        },
        "membership": [
          {
            "name": "Germination",
            "value": [0, 0, 3, 6]
          },
          {
            "name": "Tillering",
            "value": [3, 6, 8, 9]
          },
          {
            "name": "Growth",
            "value": [6, 9, 10, 12]
          },
          {
            "name": "Ripening",
            "value": [9, 12, 15, 15]
          }
        ]
      }
    ],
    "output": [
      {
        "param_name": "BobotPenyiraman",
        "universe": {
          "min": 0,
          "max": 120,
          "precision": 0.1
        },
        "membership": [
          {
            "name": "Singkat",
            "value": [0, 0, 15, 30]
          },
          {
            "name": "Lama",
            "value": [15, 30, 60, 75]
          },
          {
            "name": "SangatLama",
            "value": [60, 75, 90, 100]
          }
        ]
      }
    ],
    "rule": [
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Lama"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["SangatLama"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Lama"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["SangatLama"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["SangatLama"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["SangatLama"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["SangatLama"],
      ["SangatLama"],
      ["SangatLama"],
      ["Lama"],
      ["SangatLama"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Lama"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["SangatLama"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Lama"],
      ["SangatLama"],
      ["Lama"],
      ["Singkat"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["Lama"],
      ["Lama"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["SangatLama"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["SangatLama"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Lama"],
      ["SangatLama"],
      ["Lama"],
      ["Lama"],
      ["SangatLama"],
      ["Singkat"],
      ["Singkat"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Singkat"],
      ["Lama"],
      ["Lama"],
      ["Lama"],
      ["Singkat"],
      ["Lama"]
    ]
  }
}
```

- Universe including [min, max, precision]
- Rule will have same count as combination of input's memberships count
- Membership including 4 trapezoidal x-axis point

## Deployment

https://medium.com/geekculture/deploying-flask-application-on-vps-linux-server-using-nginx-a1c4f8ff0010
