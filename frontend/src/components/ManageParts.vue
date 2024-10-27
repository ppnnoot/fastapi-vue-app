<script>
import axios from "axios";

export default {
  name: "ManageParts",
  data() {
    return {
      partNo: [],
      newPart: "",
      selectedFile: null,
      message: "",
      partData: {
        columns: [],
        data: [],
      },
      isEditing: false, // Edit mode status
      partToDelete: null, // Part to delete
    };
  },

  methods: {
    triggerFileSelect() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      this.uploadFile();
    },
    async uploadFile() {
      if (!this.selectedFile) {
        this.message = "Please select a file first.";
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      const uploadUrls = [
        "http://fastapi-backend:80/uploadfile/",
        "http://localhost:80/uploadfile/",
        "http://127.0.0.1:80/uploadfile/",
        "http://localhost:8000/uploadfile/",
      ];
      let response;

      for (const url of uploadUrls) {
        try {
          response = await axios.post(url, formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });
          if (response.data) {
            this.message = `Uploaded ${this.selectedFile.name} successfully!`;
            this.partData = response.data.data;
            break; // Exit the loop if a valid response is received
          } else {
            throw new Error("No response data");
          }
        } catch (error) {
          if (error.response) {
            if (error.response.status === 413) {
              this.message = "File is too large. Please select a smaller file.";
            } else {
              this.message = `Error uploading file: ${error.response.data}`;
              console.error("Error uploading file:", error);
            }
          }
        }
      }
      if (!response) {
        this.message = "Error uploading file to any of the URLs.";
      }
    },
    async downloadFile() {
      // Check if there's data to download
      if (!this.partData.data.length) {
        this.uploadMessage = "No data to download.";
        return;
      }

      const firstRow = this.partData.data[0];
      if (!firstRow || !firstRow.length) {
        this.uploadMessage = "First row of data is empty.";
        return;
      }

      // Prepare column data, including "Part No"
      const columnData = [
        "Part No",
        ...this.partData.data.map((row) => row[0]),
      ];
      const indexColumnData = this.partData.data.map((_, index) => index);

      // Prepare data ensuring all rows have the same length
      const data = this.partData.data.map((row) => {
        // Ensure the length of each row matches the column data
        const adjustedRow = [...row]; // Copy the original row
        while (adjustedRow.length < columnData.length - 1) {
          adjustedRow.push(0); // Fill missing columns with 0
        }
        return adjustedRow;
      });

      const jsonData = {
        data: {
          index: indexColumnData,
          columns: columnData,
          data,
        },
      };

      // Sending data to the backend
      try {
        const response = await axios.post(
          "http://0.0.0.0/downloadfile/",
          jsonData
        );
        this.uploadMessage = "File downloaded successfully!";
      } catch (error) {
        console.error(
          "Error sending data:",
          error.response ? error.response.data : error.message
        );
        this.uploadMessage =
          "Error sending data. Please check the console for details.";
      }
    },

    addPart() {
      if (!this.newPart) {
        alert("Part number cannot be empty!");
        return;
      }

      // Validate if the part already exists
      if (this.isPartExists(this.newPart)) {
        alert("Part number already exists!");
        return;
      }

      if (this.partData.data.length !== 0) {
        this.partData.data.forEach((row) => {
          row.push(0);
        });
      }

      const newRow = this.createNewRow();
      this.partData.data.push([this.newPart, ...newRow]);
      this.newPart = "";
    },

    isPartExists(part) {
      return this.partData.data.some((row) => row[0] === part);
    },

    createNewRow() {
      const numColumns = this.partData.data.length + 1; // Update to determine the new row length
      const newRow = Array(numColumns - 1).fill(0); // Fill with 0 for all columns except the last one
      newRow.push(null);
      return newRow;
    },

    editParts() {
      this.isEditing = !this.isEditing;
    },

    deletePart(rowIndex, colIndex) {
      this.partData.data.splice(rowIndex, 1);
      // ลบค่าจากทุกแถวที่ตำแหน่ง colIndex ที่ระบุ
      this.partData.data.forEach((row) => {
        row.splice(rowIndex + 1, 1); // ลบค่าที่ตำแหน่ง rowIndex
      });
    },

    handleNumberInput(rowIndex, colIndex) {
      const currentValue = this.partData.data[rowIndex][colIndex];
      if (colIndex === 0) return; // Skip editing the part name column
      this.partData.data[rowIndex][colIndex] =
        parseFloat(this.filterToDecimal(currentValue)) || 0;
    },

    filterToDecimal(value) {
      const sanitizedValue = value.replace(/[^0-9.]/g, "");
      const decimalParts = sanitizedValue.split(".");
      return decimalParts.length > 2
        ? `${decimalParts[0]}.${decimalParts[1]}`
        : sanitizedValue;
    },
  },
};
</script>

<template>
  <div class="container">
    <h4 class="header-text">Parts Change Over Matrix</h4>
    <div class="actions-container">
      <button class="button" @click="downloadFile">Download</button>
      <div class="file-upload-container">
        <button class="button" @click="triggerFileSelect">Upload</button>
        <input
          type="file"
          ref="fileInput"
          @change="handleFileUpload"
          accept=".xlsx,.csv"
          style="display: none"
        />
        <h4 v-if="message" class="upload-message">{{ message }}</h4>
      </div>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th key="partnumber" class="cell">Part No</th>
            <th v-for="part in partData.data" class="cell">
              {{ part[0] }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in partData.data" :key="rowIndex">
            <td v-for="(value, colIndex) in row" :key="colIndex" class="cell">
              <div
                style="
                  display: flex;
                  justify-content: center;
                  align-items: center;
                  height: 100%;
                "
              >
                <input
                  type="text"
                  v-model="partData.data[rowIndex][colIndex]"
                  @input="handleNumberInput(rowIndex, colIndex)"
                  :disabled="rowIndex === colIndex - 1"
                  class="input-part"
                  :style="{
                    backgroundColor:
                      colIndex === 0
                        ? '#bababa'
                        : rowIndex === colIndex - 1
                        ? 'lightgray'
                        : 'transparent',
                  }"
                />
                <button
                  v-if="isEditing && colIndex === 0"
                  @click="deletePart(rowIndex)"
                  class="delete-button"
                >
                  <span class="material-symbols-outlined">delete</span>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div>
      <div class="cell-input">
        <input v-model="newPart" placeholder="New Part" class="input-part" />
      </div>
      <div style="display: flex; gap: 1rem; padding-top: 10px">
        <button @click="addPart" class="button">Add Part</button>
        <button @click="editParts" class="button">Edit</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.header-text {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
}

.table-container {
  overflow-x: auto; /* Enable horizontal scrolling */
  overflow-y: auto; /* Enable vertical scrolling */
  margin-top: 20px;
  max-width: 100%; /* Full width responsive */
  max-height: 800px; /* Maximum height for vertical scrolling */
  border: 1px solid #ccc;
}

.actions-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.file-upload-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.upload-message {
  color: #2e8b57;
}

table {
  border-collapse: collapse;
  font-size: 16px;
  table-layout: auto;
  width: max-content;
}

.cell {
  align-items: center;
  border: 1px solid #ccc;
  height: 40px;
  width: 100px;
  box-sizing: border-box;
  padding: 0;
}

.cell-input {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ccc;
  height: 40px;
  width: 100px;
  box-sizing: border-box;
  padding: 0;
}

.input-part {
  width: 100%;
  height: 100%;
  font-size: 14px;
  padding: 8px;
  border: none;
  background-color: transparent;
  outline: none;
  text-align: center;
}

thead {
  background-color: #bababa;
}

.button {
  min-width: 100px;
  background-color: #ccc;
  color: #333;
  border: none;
  border-radius: 5px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button:hover {
  background-color: #999;
}

.remove-button {
  background-color: #ff6347;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.remove-button:hover {
  background-color: #cc4b37;
}

.delete-button {
  background: none;
  margin: 0 5px;
  border: 1px solid #ff6347;
  border-radius: 2px;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-button span {
  font-size: 18px;
  color: #ff6347;
  transition: transform 0.2s;
}

.delete-button:hover {
  transform: scale(1.2);
}
</style>
