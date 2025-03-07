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
    });

    // Handle menu click for Keyword Research
    document.getElementById("keyword-research").onclick = function() {
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
            contextMenu.style.display = "none";
        });
    };

    // Handle menu click for Pre Translation
    document.getElementById("pre-translation").onclick = function() {
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
            contextMenu.style.display = "none";
        });
    };

    document.getElementById("search-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission
        
        let searchTerm = document.getElementById("search-box").value.trim();
        if (!searchTerm) return; // Don't proceed if search box is empty
        
        // Show loading spinner while waiting for response
        updateContextPane("", true);
        
        // The server is returning a 500 error, which suggests a server-side issue
        // Let's check the server code in app-server.py for the glossary function
        // The issue might be in the JSON handling on the server side
        
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
            // Provide more helpful error message to debug the server issue
            updateContextPane("Server error occurred. Check the server logs for more details.", false);
            
            // The 500 error suggests the server code has an issue, possibly in the glossary function
            // The error about "<!doctype" suggests HTML is being returned instead of JSON
            // This often happens when the server crashes and returns an error page
        });
    });

    // Handle menu click for Pre Translation
    document.getElementById("lookup-glossary").onclick = function() {
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
            contextMenu.style.display = "none";
        });
    };

    // Handle menu click for Pre Translation
    document.getElementById("find-examples").onclick = function() {
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
            contextMenu.style.display = "none";
        });
    };

    // Handle menu click for Pre Translation
    document.getElementById("explain-grammar").onclick = function() {
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
            contextMenu.style.display = "none";
        });
    };

    
    function updateContextPane(text, isLoading = false) {
        if (!contextPane) return;
    
        if (isLoading) {
            // Ensure spinner is visible and remove existing text
            contextPane.innerHTML = `<div class="loading-spinner"></div>`;
            document.querySelector(".loading-spinner").style.display = "block"; // Ensure spinner is displayed
        } else {
            // Remove spinner and show the actual response
            contextPane.innerHTML = `<p>${text}</p>`;
        }
    }

    // Hide context menu when clicking elsewhere
    document.addEventListener("click", function() {
        contextMenu.style.display = "none";
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

    // For each editable cell, trigger autosave on blur
    const editableCells = document.querySelectorAll('.translation-table td[contenteditable="true"]');
    editableCells.forEach(cell => {
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


});