document.addEventListener("DOMContentLoaded", function() {
    
    const table = document.querySelector(".translation-table");
    
    // Create custom context menu
    const contextMenu = document.createElement("div");
    contextMenu.id = "custom-context-menu";
    contextMenu.innerHTML = `<ul>
    <li id="keyword-research">Research Keywords</li>
    <li id="pre-translation">Suggest Translation</li>
    <li id="lookup-glossary">Lookup Glossary</li>
    <li id="find-examples">Find Examples</li>
    <li id="explain-grammar">Explain Grammar</li>
    </ul>`;
    document.body.appendChild(contextMenu);

    let selectedText = "";
    let selectedRange = null;
    let contextPane = document.querySelector(".context-pane");

    // Add loading spinner inside context pane
    const spinner = document.createElement("div");
    spinner.classList.add("loading-spinner");
    contextPane.appendChild(spinner);

    // Function to restore text selection
    function restoreSelection() {
        if (selectedRange) {
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(selectedRange);
        }
    }

    // Prevent clicks on the context menu from clearing the selection
    contextMenu.addEventListener("click", function(event) {
        event.stopPropagation();
    });

    // Show custom context menu on right-click
    table.addEventListener("contextmenu", function(event) {
        let selection = window.getSelection();
        selectedText = selection.toString().trim();
        if (!selectedText) return;

        event.preventDefault(); // Prevent default menu

        selectedRange = selection.getRangeAt(0);

        // Get viewport and document scroll positions
        let viewportWidth = window.innerWidth;
        let viewportHeight = window.innerHeight;
        let scrollY = window.scrollY;
        let scrollX = window.scrollX;

        // Get context menu dimensions
        contextMenu.style.display = "block";  // Ensure menu is visible before measuring
        let menuWidth = contextMenu.offsetWidth;
        let menuHeight = contextMenu.offsetHeight;

        // Default positioning
        let menuX = event.clientX + scrollX;
        let menuY = event.clientY + scrollY;

        // Prevent overflow on right side
        if (menuX + menuWidth > document.body.clientWidth) {
            menuX = document.body.clientWidth - menuWidth - 10; // Add padding
        }

        // Prevent overflow at bottom
        if (menuY + menuHeight > document.body.clientHeight + scrollY) {
            menuY = document.body.clientHeight + scrollY - menuHeight - 10;
        }

        // Set the new position
        contextMenu.style.top = `${menuY}px`;
        contextMenu.style.left = `${menuX}px`;
        contextMenu.style.display = "block";
        
        // Ensure selection is maintained
        restoreSelection();
    });

    // Handle menu click for Keyword Research
    document.getElementById("keyword-research").onclick = function(event) {
        event.stopPropagation(); // Prevent the click from bubbling up
        contextMenu.style.display = "none";  // Hide menu immediately before request
        updateContextPane("", true); // Show spinner

        fetch("/keyword-research", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: selectedText })
        })
        .then(response => response.json())
        .then(data => {
            updateContextPane(data.result, false); // Hide spinner & show result
            restoreSelection(); // Restore the selection after the action
        });
    };

    // Handle menu click for Pre Translation
    document.getElementById("pre-translation").onclick = function(event) {
        event.stopPropagation(); // Prevent the click from bubbling up
        contextMenu.style.display = "none";  // Hide menu before API call
        updateContextPane("", true); // Show spinner

        fetch("/pre-translation", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: selectedText })
        })
        .then(response => response.json())
        .then(data => {
            updateContextPane(data.result, false); // Hide spinner & show result
            restoreSelection(); // Restore the selection after the action
        });
    };

    document.getElementById("search-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission
        
        let searchTerm = document.getElementById("search-box").value.trim();
        if (!searchTerm) return; // Don't proceed if search box is empty
        
        // Show loading spinner while waiting for response
        updateContextPane("", true);
        
        const formData = new FormData();
        formData.append('search_term', searchTerm);
        
        fetch("/glossary", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            updateContextPane(data.result, false); // Hide spinner & show result
        })
        .catch(error => {
            console.error("Error:", error);
            updateContextPane("Server error occurred. Check the server logs for more details.", false);
        });
    });

    // Handle menu click for Lookup Glossary
    document.getElementById("lookup-glossary").onclick = function(event) {
        event.stopPropagation(); // Prevent the click from bubbling up
        contextMenu.style.display = "none";  // Hide menu before API call
        updateContextPane("", true); // Show spinner

        fetch("/lookup-glossary", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: selectedText })
        })
        .then(response => response.json())
        .then(data => {
            updateContextPane(data.result, false); // Hide spinner & show result
            restoreSelection(); // Restore the selection after the action
        });
    };

    // Handle menu click for Find Examples
    document.getElementById("find-examples").onclick = function(event) {
        event.stopPropagation(); // Prevent the click from bubbling up
        contextMenu.style.display = "none";  // Hide menu before API call
        updateContextPane("", true); // Show spinner

        fetch("/find-examples", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: selectedText })
        })
        .then(response => response.json())
        .then(data => {
            updateContextPane(data.result, false); // Hide spinner & show result
            restoreSelection(); // Restore the selection after the action
        });
    };

    // Handle menu click for Explain Grammar
    document.getElementById("explain-grammar").onclick = function(event) {
        event.stopPropagation(); // Prevent the click from bubbling up
        contextMenu.style.display = "none";  // Hide menu before API call
        updateContextPane("", true); // Show spinner

        fetch("/explain-grammar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: selectedText })
        })
        .then(response => response.json())
        .then(data => {
            updateContextPane(data.result, false); // Hide spinner & show result
            restoreSelection(); // Restore the selection after the action
        });
    };

    
    function updateContextPane(text, isLoading = false, isHTML = false) {
        if (!contextPane) return;
    
        if (isLoading) {
            // Ensure spinner is visible and remove existing text
            contextPane.innerHTML = `<div class="loading-spinner"></div>`;
            document.querySelector(".loading-spinner").style.display = "block"; // Ensure spinner is displayed
        } else if (text === "") {
            // Clear the context pane if text is empty
            contextPane.innerHTML = "";
        } else if (isHTML) {
            // If it's already HTML content, insert it directly
            contextPane.innerHTML = text;
        } else {
            // Check if the text contains HTML tags
            const containsHTML = /<[a-z][\s\S]*>/i.test(text);
            
            // If it contains HTML, insert it directly; otherwise, wrap in paragraph tags
            if (containsHTML) {
                contextPane.innerHTML = text;
            } else {
                // Replace newlines with <br> tags for better formatting
                const formattedText = text.replace(/\n/g, '<br>');
                contextPane.innerHTML = `<p>${formattedText}</p>`;
            }
        }
    }

    // Hide context menu when clicking elsewhere
    document.addEventListener("click", function(event) {
        if (!contextMenu.contains(event.target)) {
            contextMenu.style.display = "none";
        }
    });

    let autoSaveTimer = null;

    function resetAutoSaveTimer(cell) {
        // Clear any existing timer
        if (autoSaveTimer) clearTimeout(autoSaveTimer);
        // Set a new timer for 1 minute (60000 ms)
        autoSaveTimer = setTimeout(() => autoSave(cell), 60000);
    }

    function autoSave(cell) {
        const rowIndex = cell.closest("tr").rowIndex - 1; // Adjust for header row
        fetch("/autosave", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ row: rowIndex, content: cell.innerText })
        });
    }
    
    // For each editable cell, trigger a timer reset on focus
    document.querySelectorAll('.translation-table td[contenteditable="true"]').forEach(cell => {
        cell.addEventListener('focus', function() {
            resetAutoSaveTimer(cell);
        });
        // Also auto-save immediately on blur
        cell.addEventListener('blur', function() {
            autoSave(cell);
        });
    });

    document.querySelectorAll('.translation-table td[contenteditable="true"]').forEach(cell => {
        cell.addEventListener('blur', function() {
            autoSave(cell);
        });
    });

    document.querySelectorAll('.target-text').forEach(cell => {
        cell.addEventListener('keydown', function(event) {
            if (event.key === "Enter") {
                event.preventDefault(); // Prevent default newline behavior
                
                if (event.shiftKey) {
                    // Shift + Enter: Insert a line break inside the cell
                    document.execCommand('insertLineBreak');
                } else {
                    // Regular Enter: Move to the next row in column 2
                    let nextRow = this.closest('tr').nextElementSibling;
                    if (nextRow) {
                        let nextCell = nextRow.querySelector('.target-text');
                        if (nextCell) nextCell.focus();
                    }
                }
            }
        });
    });

    // Enable arrow key navigation in column 2 (target-text)
    document.querySelectorAll('.target-text').forEach(cell => {
        cell.addEventListener('keydown', function(event) {
            let currentRow = this.closest('tr');

            if (event.key === "ArrowDown") {
                event.preventDefault(); // Prevent page scrolling
                let nextRow = currentRow.nextElementSibling;
                if (nextRow) {
                    let nextCell = nextRow.querySelector('.target-text');
                    if (nextCell) nextCell.focus();
                }
            } else if (event.key === "ArrowUp") {
                event.preventDefault(); // Prevent page scrolling
                let prevRow = currentRow.previousElementSibling;
                if (prevRow) {
                    let prevCell = prevRow.querySelector('.target-text');
                    if (prevCell) prevCell.focus();
                }
            }
        });
    });

    document.querySelector(".context-pane").addEventListener("wheel", function(event) {
        let canScroll = this.scrollHeight > this.clientHeight;
        let isScrollingUp = event.deltaY < 0;
        let isScrollingDown = event.deltaY > 0;
        let atTop = this.scrollTop === 0;
        let atBottom = this.scrollTop + this.clientHeight >= this.scrollHeight - 1;
    
        if (canScroll) {
            if ((isScrollingUp && !atTop) || (isScrollingDown && !atBottom)) {
                event.stopPropagation(); // Allow scroll inside context pane without blocking
            } else {
                event.preventDefault(); // Prevent further scrolling beyond the limits
            }
        }
    }, { passive: false });

    document.getElementById('context-back').addEventListener('click', () => {
        fetch('/history?direction=back')
          .then(res => res.json())
          .then(data => updateContextPane(data.result, false));
      });
      
    document.getElementById('context-forward').addEventListener('click', () => {
        fetch('/history?direction=forward')
          .then(res => res.json())
          .then(data => updateContextPane(data.result, false));
    });

    // Function to get row index from a cell
    function getRowIndex(cell) {
        // Subtract 1 to account for the header row
        // This ensures the first data row has index 0, matching the server-side indexing
        return Array.from(cell.closest('tbody').children).indexOf(cell.closest('tr')) - 1;
    }
    
    // Function to load context data for a specific row
    function loadContextForRow(rowIndex) {
        console.log("Loading context for row:", rowIndex);
        updateContextPane("", true); // Show spinner
        
        fetch("/get-context", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ row_index: rowIndex })
        })
        .then(response => {
            console.log("Response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data);
            if (data.has_content) {
                // If there's content, display it (already formatted with heading)
                console.log("Has content, displaying:", data.result);
                updateContextPane(data.result, false, true); // true for HTML content
            } else {
                // If no content, display "No annotations" message
                console.log("No content, displaying 'No annotations'");
                const noAnnotationsHtml = `<h3 class="no-annotations-heading">No annotations</h3>
                <div class="no-annotations-content">No review comments available for this text.</div>`;
                updateContextPane(noAnnotationsHtml, false, true); // true for HTML content
            }
        })
        .catch(error => {
            console.error("Error loading context:", error);
            updateContextPane("Error loading context data", false);
        });
    }
    
    // Add event listeners to target cells to show context data when selected
    document.querySelectorAll('.target-text').forEach(cell => {
        cell.addEventListener('focus', function() {
            const originalIndex = Array.from(cell.closest('tbody').children).indexOf(cell.closest('tr'));
            const rowIndex = getRowIndex(this);
            console.log("Target cell focused, original index:", originalIndex, "adjusted index:", rowIndex);
            loadContextForRow(rowIndex);
        });
    });
});