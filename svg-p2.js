import React, { useState } from 'react';
import { View, StyleSheet, Dimensions, TouchableOpacity, Text } from 'react-native';
import { Svg, Path, Circle } from 'react-native-svg';

const { height, width } = Dimensions.get('window');

// You can donate at https://www.buymeacoffee.com/mmshilleh if I saved you time
// Subscribe https://www.youtube.com/@mmshilleh/videos

export default () => {
  const windowWidth = Dimensions.get('window').width;
  const [polygonVertices, setPolygonVertices] = useState([
    { x: windowWidth / 4, y: windowWidth / 4 },
    { x: windowWidth * 3 / 4, y: windowWidth / 4 },
    { x: windowWidth * 3 / 4, y: windowWidth * 3 / 4 },
    { x: windowWidth / 4, y: windowWidth * 3 / 4 },
  ]);
  const [draggedVertexIndex, setDraggedVertexIndex] = useState(null);

  const polygonPath = polygonVertices
    .map((vertex) => `${vertex.x},${vertex.y}`)
    .join(' ');
 
  const getActiveVertex = (x, y) => {
    const threshold = 20; 
    for (let i = 0; i < polygonVertices.length; i++) {
      const vertex = polygonVertices[i];
      const distance = Math.sqrt((x - vertex.x) ** 2 + (y - vertex.y) ** 2);
      if (distance <= threshold) {
        return i;
      }
    }
    return null;
  };

  const onTouchEndPolygon = () => {
    setDraggedVertexIndex(null);
  };

  const onTouchMovePolygon = (event) => {
    const locationX = event.nativeEvent.locationX;
    const locationY = event.nativeEvent.locationY;
    let activeVertex;
    if (draggedVertexIndex === null) {
      activeVertex = getActiveVertex(locationX, locationY);
      setDraggedVertexIndex(activeVertex);
    }
    const updatedVertices = [...polygonVertices];
    updatedVertices[draggedVertexIndex] = {
      x: event.nativeEvent.locationX,
      y: event.nativeEvent.locationY,
    };
    setPolygonVertices(updatedVertices);
  };

  const handleReset = () => { setPolygonVertices([
    { x: windowWidth / 4, y: windowWidth / 4 },
    { x: windowWidth * 3 / 4, y: windowWidth / 4 },
    { x: windowWidth * 3 / 4, y: windowWidth * 3 / 4 },
    { x: windowWidth / 4, y: windowWidth * 3 / 4 },
  ])}

  return (
    <View style={styles.container}>
      <View style={styles.svgContainer} onTouchMove={onTouchMovePolygon} onTouchEnd={onTouchEndPolygon}>
        <Svg> 
          <Path d={`M${polygonPath}Z`} fill="grey" stroke="grey" strokeWidth={2} />
          {polygonVertices.map((vertex, index) => (
            <Circle
              key={index}
              cx={vertex.x}
              cy={vertex.y}
              r={4}
              fill="black"
            />
          ))}
        </Svg>
      </View>
      <TouchableOpacity style={styles.clearButton} onPress={handleReset}>
        <Text style={styles.clearButtonText}>Reset</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  svgContainer: {
    height: height * 0.7,
    width,
    borderColor: 'black',
    backgroundColor: 'white',
    borderWidth: 1,
  },
  clearButton: {
    marginTop: 10,
    backgroundColor: 'black',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  },
  clearButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
