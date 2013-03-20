;;; ==============================================
;;; simple-tigernote.el --- edit local raw tigernote pages
;; Copyright (C) 2002, 2003  Alex Schroeder

;; Author: Alex Schroeder <alex@gnu.org>
;;         David Hansen <david.hansen@physik.fu-berlin.de>
;; Maintainer: David Hansen <david.hansen@physik.fu-berlin.de>
;; Version: 1.0.9
;; Keywords: hypermedia
;; URL: http://www.emacswiki.org/cgi-bin/wiki.pl?SimpleWikiEditMode

;; This file is not part of GNU Emacs.

;; This is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 2, or (at your option)
;; any later version.

;; This is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with GNU Emacs; see the file COPYING.  If not, write to the
;; Free Software Foundation, Inc., 59 Temple Place - Suite 330,
;; Boston, MA 02111-1307, USA.
;; ==================================================
;;; Modified from simple-wiki.el, Gao Wang 2012
;;
;;; Commentary:

;; Use `simple-tigernote-mode' to edit raw tigernote pages.  This is useful for
;; temp files when editing textareas in w3m, for example.  Here is how
;; to do that:
;;
;; (add-to-list 'auto-mode-alist '("w3mtmp" . simple-tigernote-mode))

;;; Code:

(require 'font-lock)

(defvar simple-tigernote-version "1.0.9")

(defvar simple-tigernote-common-hook nil
  "Hook to run in every simple-tigernote mode.")



;; the default value are for the emacstigernote

(defvar simple-tigernote-tag-list
  ;; xemacs requires an alist for `completing-read'.
  '(("u" . nil) ("b" . nil) ("i" . nil) ("strong" . nil) ("em" . nil)
    ("notigernote" . nil) ("code" . nil) ("tt" . nil) ("pre". t))
  "Alist of supported tags used for `completing-read'.
The cdr of a pair is non-nil if a newline should be inserted after the
opening tag.")

(if (featurep 'xemacs) ;; xemacs doesn't know character classes
    (defvar simple-tigernote-link-pattern
      ;; c&p from oddmuse sources, weird doesn't work perfectly so use
      ;; a different for gnu emacs
      '("\\<\\([A-Z]+[a-z\x80-\xff]+[A-Z][A-Za-z\x80-\xff]*\\)" . 0)
      "The pattern matching camel case links.
A Pair of the pattern and the matching subexpression.")
  (defvar simple-tigernote-link-pattern
    '("\\<\\([A-Z]+?[[:lower:][:nonascii:]]+?[A-Z][[:lower:][:upper:]]*\\)" . 0)
    "The pattern matching camel case links.
A Pair of the pattern and the matching subexpression."))

(defvar simple-tigernote-free-link-pattern
  '(" \\[\\([^\n]+?\\)\\] " . 1)
  "The Pattern matching free links.
A Pair of the pattern and the matching subexpression.")

(defvar simple-tigernote-em-patterns
  '(("\\(\\W\\|^\\)\"\\([^\"]\\|[^\"]\"\\)*\"" . 0)        ; ''emph''
    ("\\(\\W\\|^\\)\"\"\\([^\"]\\|[^\"]\"\\)*\"\"" . 0)      ; '''strong'''
    ("\\(\\W\\|^\\)\"\"\"\\([^\"]\\|[^\"]\"\\)*\"\"\"" . 0)) ; '''''strong emph'''''
  "List of regexps to match emphasized, strong and strong emphasized text.
Actually a list of pairs with the pattern and the number of the matching
subexpression.")

(defvar simple-tigernote-headline-patterns
  '(("^###\n#! \\([^\n!]+\\)\n###$" . 1)
    ("^###\n#\\([^\n!]+\\)\n###$" . 1)
    ("^#! \\([^\n!]+\\)$" . 1)
    ("^#!! \\([^\n!]+\\)$" . 1)
    )
  "List of regexps to match headlines.
Actually a list of pairs with the pattern and the number of the matching
subexpression.")

(defvar simple-tigernote-smilies-pattern
  (cons (concat
         "[ \t]\\("
         ":-?D\\|:-?)\\|;-?\)\\|:-?]\\|8-\)\\|"
         ":-\\\\|\\|:-?[/\\\\]\\|:-?(\\|:-?{\\)"
         "\\W") 1)
  "Pair of the pattern used to match smilies an the matching subexpression.")

(defvar simple-tigernote-outline-patterns
  '("=+" . "=+[ \t]*\n")
  "Pair of patterns for `outline-regexp' and `outline-heading-end-regexp'.")

(defvar simple-tigernote-horiz-line-pattern
  '("-----*" . 0)
  "Pair of the pattern use to match a horizontal line and the subexpression.")

(defvar simple-tigernote-line-break-pattern
  'none
  "Pair of the pattern used to match a line break and matching subexpression.")

(defvar simple-tigernote-enum-pattern
  '("^\\([*#]*#+\\)\\([^#*]\\|$\\)" . 1)
  "Pair of the pattern to match an entry of a numbered list the subexpression.")

(defvar simple-tigernote-bullet-pattern
  '("^\\([*#]*\\*+\\)\\([^*#]\\|$\\)" . 1)
  "Pair of the pattern to match an entry of a bullet list the subexpression.")

(defvar simple-tigernote-indent-pattern
  '("^:+" . 0)
  "Pair of the pattern to match indented text and the matching subexpression.")

(defvar simple-tigernote-definition-pattern
  '("^\\(;+.*?:\\)" . 1)
  "Pair of the pattern to match definition lists and the subexpression.")

(defvar simple-tigernote-em-strings
  '("\"" . "\"")
  "Start and end string for emphasis text.")

(defvar simple-tigernote-strong-strings
  '("\"\"" . "\"\"")
  "Start and end strings for strong text.")

(defvar simple-tigernote-strong-em-strings
  '("\"\"\"" . "\"\"\"")
  "Start and end string for strong text.")

(defvar simple-tigernote-additional-keywords
  (list
   ;; time stamp at the beginning of the buffer
   '("\\`\\([0-9]+\\)[ \t]+\\(#.+?\\)\n"
     (1 font-lock-constant-face)
     (2 font-lock-warning-face))
   '("{\$\\([^\$]\\|[^\$]\$\\)*\$}" . font-lock-keyword-face) ; {$a .. b$}
   '("@@[^ \t@][^@]*[^ \t@]@@" . font-lock-string-face) ; @@a .. b@@
   '(simple-tigernote-match-tag-i . (0 'simple-tigernote-italic-face append))
   '(simple-tigernote-match-tag-b . (0 'simple-tigernote-bold-face append))
   '(simple-tigernote-match-tag-u . (0 'simple-tigernote-underline-face append))
   '(simple-tigernote-match-tag-tt . (0 'simple-tigernote-teletype-face append))
   '(simple-tigernote-match-tag-em . (0 'simple-tigernote-emph-face append))
   '(simple-tigernote-match-tag-strong . (0 'simple-tigernote-strong-face append))

   ;; tags FIXME: oddmuse knows no parameters
   (list (concat "\\(</?\\)"
                 "\\([A-Za-z]+\\)"
                 "\\(\\([ \t]+[a-zA-Z]+\\)=\\(\".*\"\\)\\)*"
                 "\\(/?>\\)?")
         '(1 'default t t)
         '(2 'font-lock-function-name-face t t)
         '(4 'font-lock-variable-name-face t t)
         '(5 'font-lock-string-face t t)
         '(6 'default t t))

   '(simple-tigernote-match-tag-notigernote . (0 'simple-tigernote-notigernote-face t))

   ;; code blocks
   '(simple-tigernote-match-tag-code . (0 'simple-tigernote-code-face t))
   '(simple-tigernote-match-tag-pre . (0 'simple-tigernote-code-face t))

   '(simple-tigernote-match-code-block . (0 'simple-tigernote-code-face t)))

  "Additional keywords for font locking.")

(defvar simple-tigernote-font-lock-keywords nil
  "Font lock keywords for simple tigernote mode.")

(defvar simple-tigernote-tag-history nil
  "History for `completing-read' of tags.")



;; custom groups

(defgroup simple-tigernote ()
  "Edit raw tigernote pages.")

(defgroup simple-tigernote-faces ()
  "Faces simple-tigernote-mode." :group 'simple-tigernote)



;; faces

;; xemacs doesn't know about :inherit.  Just set all heading to bold.
(if (featurep 'xemacs)
    (progn
      (defface simple-tigernote-heading-1-face
        '((t (:bold t)))
        "Face for Tigernote headings at level 1."
        :group 'simple-tigernote-faces)

      (defface simple-tigernote-heading-2-face
        '((t (:bold t)))
        "Face for Tigernote headings at level 2."
        :group 'simple-tigernote-faces)

      (defface simple-tigernote-heading-3-face
        '((t (:bold t)))
        "Face for Tigernote headings at level 3."
        :group 'simple-tigernote-faces)

      (defface simple-tigernote-heading-4-face
        '((t (:bold t)))
        "Face for Tigernote headings at level 4."
        :group 'simple-tigernote-faces)

      (defface simple-tigernote-heading-5-face
        '((t (:bold t)))
        "Face for Tigernote headings at level 5."
        :group 'simple-tigernote-faces)

      (defface simple-tigernote-heading-6-face
        '((t (:bold t)))
        "Face for Tigernote headings at level 6."
        :group 'simple-tigernote-faces))

  (defface simple-tigernote-heading-1-face
    '((((type tty pc) (class color)) (:foreground "yellow" :weight bold))
      (t (:height 1.2 :inherit simple-tigernote-heading-2-face)))
    "Face for Tigernote headings at level 1."
    :group 'simple-tigernote-faces)

  (defface simple-tigernote-heading-2-face
    '((((type tty pc) (class color)) (:foreground "lightblue" :weight bold))
      (t (:height 1.2 :inherit simple-tigernote-heading-3-face)))
    "Face for Tigernote headings at level 2."
    :group 'simple-tigernote-faces)

  (defface simple-tigernote-heading-3-face
    '((((type tty pc) (class color)) (:weight bold))
      (t (:height 1.2 :inherit simple-tigernote-heading-4-face)))
    "Face for Tigernote headings at level 3."
    :group 'simple-tigernote-faces)

  (defface simple-tigernote-heading-4-face
    '((((type tty pc) (class color)) (:weight bold))
      (t (:weight bold :inherit variable-pitch)))
    "Face for Tigernote headings at level 4."
    :group 'simple-tigernote-faces)

  (defface simple-tigernote-heading-5-face
    '((((type tty pc) (class color)) (:weight bold))
      (t (:weight bold :inherit variable-pitch)))
    "Face for Tigernote headings at level 5."
    :group 'simple-tigernote-faces)

  (defface simple-tigernote-heading-6-face
    '((((type tty pc) (class color)) (:weight bold))
      (t (:weight bold :inherit variable-pitch)))
    "Face for Tigernote headings at level 6."
    :group 'simple-tigernote-faces))

(defface simple-tigernote-emph-face
  '((t (:italic t)))
  "Face for ''emphasis''."
  :group 'simple-tigernote-faces)

(defface simple-tigernote-strong-face
  '((t (:bold t)))
  "Face for '''strong emphasis'''."
  :group 'simple-tigernote-faces)

(defface simple-tigernote-strong-emph-face
  '((t (:bold t :italic t)))
  "Face for '''''stronger emphasis'''''."
  :group 'simple-tigernote-faces)

(defface simple-tigernote-italic-face
  '((t (:italic t)))
  "Face for <i>italic</i>."
  :group 'simple-tigernote-faces)

(defface simple-tigernote-bold-face
  '((t (:bold t)))
  "Face for <b>bold</b>."
  :group 'simple-tigernote-faces)

(if (featurep 'xemacs)
    (defface simple-tigernote-strike-face
      '((t (:strikethru t)))
      "Face for <strike>strike</strike>."
      :group 'simple-tigernote-faces)
  (defface simple-tigernote-strike-face
    '((t (:strike-through t)))
    "Face for <strike>strike</strike>."
    :group 'simple-tigernote-faces))

(defface simple-tigernote-underline-face
  '((t (:underline t)))
  "Face for <u>underline</u>."
  :group 'simple-tigernote-faces)

(defface simple-tigernote-local-link-face
  '((((class color) (background dark))
     (:foreground "skyblue3" :bold t))
    (((class color) (background light))
     (:foreground "royal blue" :bold t)))
  "Face for links to pages on the same tigernote."
  :group 'simple-tigernote-faces)

(defface simple-tigernote-teletype-face
  '((((class color) (background dark)) (:background "grey15"))
    (((class color) (background light)) (:background "moccasin")))
  "Face for <tt>teletype</tt>."
  :group 'simple-tigernote-faces)

(defface simple-tigernote-code-face
  '((((class color) (background dark)) (:background "grey15"))
    (((class color) (background light)) (:background "moccasin")))
  "Face for code in Tigernote pages."
  :group 'simple-tigernote-faces)

(defface simple-tigernote-notigernote-face
  '((((class color) (background dark))
     (:foreground "LightGoldenRod2"))
    (((class color) (background light))
     (:foreground "DarkGoldenRod2")))
  "Face for links to pages on the same tigernote."
  :group 'simple-tigernote-faces)

(defface simple-tigernote-smiley-face
  '((((class color) (background dark))
     (:foreground "gold" :bold t))
    (((class color) (background light))
     (:foreground "goldenrod" :bold t)))
  "Face for links to pages on the same tigernote."
  :group 'simple-tigernote-faces)



;; font lock matcher

(defun simple-tigernote-match-tag (tag limit)
  "Font lock matcher for regions within <TAG></TAG>."
  (when (search-forward (concat "<" tag ">") limit t)
    (let ((beg (match-end 0)) end)
      (if (search-forward (concat "</" tag ">") limit t)
          (setq end (match-beginning 0))
        (setq end (point)))
      (store-match-data (list beg end))
      t)))

(dolist (tag '("i" "b" "u" "tt" "notigernote" "code" "pre" "em"
               "strong" "math" "strike" "verbatim"))
  (eval `(defun ,(intern (concat "simple-tigernote-match-tag-" tag)) (limit)
           (simple-tigernote-match-tag ,tag limit))))

(defun simple-tigernote-end-of-code-block ()
  "Return the end of a code block if the cursor is within a code block.
Return nil otherwise."
  ;; FIXME: we assume that the line before code is empty.
  ;; this is not necessary in all cases.  known issues:
  ;;        (a) code starts directly after a heading.
  (save-excursion
    (backward-paragraph)
    (when (string-match "^$" (buffer-substring (point-at-bol) (point-at-eol)))
      (forward-line 1))
    (let ((char (char-after (point))))
      (when (and char (or (= char ?\t) (= char ? )))
        (forward-paragraph)
        (point)))))

(defun simple-tigernote-match-code-block (limit)
  (let (beg end)
    (when (re-search-forward "^[ \t]+[^ \t\n]" limit t)
      (setq beg (match-beginning 0))
      (setq end (simple-tigernote-end-of-code-block))
      (when end
        (if  (<= end beg)
            nil
          (store-match-data (list beg end))
          t)))))

(defun simple-tigernote-match-code-jsp (limit)
  "Match regions of preformated text in jsp tigernotes."
  (when (search-forward "{{{" limit t)
    (let ((beg (match-end 0)) end)
      (if (search-forward "}}}" limit t)
          (setq end (match-beginning 0))
        (setq end (point)))
      (store-match-data (list beg end))
      t)))



;; editing functions

(defun simple-tigernote-strings-around-region (min max strmin strmax)
  "Insert the strings STRMIN and STRMAX at positions MIN and MAX."
  (save-excursion
    (goto-char min)
    (insert strmin)
    (goto-char (+ max (length strmin)))
    (insert strmax)))

(defun simple-tigernote-emph-region (min max)
  "Marke up text of the region emphasized."
  (interactive "r")
  (if (equal simple-tigernote-em-strings 'none)
      (error "No emphasis strings defined.")
    (simple-tigernote-strings-around-region
     min max
     (car simple-tigernote-em-strings)
     (cdr simple-tigernote-em-strings))))

(defun simple-tigernote-strong-region (min max)
  "Marke up text of the region strong."
  (interactive "r")
  (if (equal simple-tigernote-strong-strings 'none)
      (error "No strong strings defined.")
    (simple-tigernote-strings-around-region
     min max
     (car simple-tigernote-strong-strings)
     (cdr simple-tigernote-strong-strings))))

(defun simple-tigernote-strong-emph-region (min max)
  "Mark up text of the region strong emphasized."
  (interactive "r")
  (if (equal simple-tigernote-strong-em-strings 'none)
      (error "No strong emphasis strings defined.")
    (simple-tigernote-strings-around-region
     min max
     (car simple-tigernote-strong-em-strings)
     (cdr simple-tigernote-strong-em-strings))))

(defun simple-tigernote-insert-around-pos (before-str after-str)
  "Insert strings BEFORE-STR and AFTER-STR before and after the cursor."
  (insert before-str)
  (save-excursion (insert after-str)))

(defun simple-tigernote-insert-emph ()
  "Insert emphasized text."
  (interactive)
  (if (equal simple-tigernote-em-strings 'none)
      (error "No emphasis strings defined.")
    (simple-tigernote-insert-around-pos
     (car simple-tigernote-em-strings)
     (cdr simple-tigernote-em-strings))))

(defun simple-tigernote-insert-strong ()
  "Insert strong text."
  (interactive)
  (if (equal simple-tigernote-strong-strings 'none)
      (error "No strong strings defined.")
    (simple-tigernote-insert-around-pos
     (car simple-tigernote-strong-strings)
     (cdr simple-tigernote-strong-strings))))

(defun simple-tigernote-insert-strong-emph ()
  "Insert strong emphasized text."
  (interactive)
  (if (equal simple-tigernote-strong-em-strings 'none)
      (error "No strong emphasis strings defined.")
    (simple-tigernote-insert-around-pos
     (car simple-tigernote-strong-em-strings)
     (cdr simple-tigernote-strong-em-strings))))

(defun simple-tigernote-insert-tag-string (tag &optional closing)
  "Insert a the string \"<TAG>\" or \"</TAG>\" if CLOSING is non-nil."
  (when (and tag (not (string= tag "")))
    (if closing (insert "</") (insert "<"))
    (insert tag)
    (insert ">")))

(defun simple-tigernote-get-tag ()
  (let (prompt)
    (if (and simple-tigernote-tag-history (car simple-tigernote-tag-history))
        (setq prompt (concat "Tag (" (car simple-tigernote-tag-history) "): "))
      (setq prompt "Tag: "))
    (setq tag (completing-read prompt simple-tigernote-tag-list nil nil ""
                               'simple-tigernote-tag-history
                               (car simple-tigernote-tag-history))))
  (unless (assoc tag simple-tigernote-tag-list)
    (add-to-list 'simple-tigernote-tag-list (cons tag nil)))
  tag)

(defun simple-tigernote-tag-region (min max &optional tag)
  "Insert opening and closing text at begin and end of the region."
  (interactive "r")
  (unless tag
    (setq tag (simple-tigernote-get-tag)))
  (let ((taglen (+ 2 (length tag))))
    (save-excursion
      (goto-char min)
      (simple-tigernote-insert-tag-string tag)
      (when (and (assoc tag simple-tigernote-tag-list)
                 (cdr (assoc tag simple-tigernote-tag-list)))
        (setq taglen (1+ taglen))
        (insert "\n"))
      (goto-char (+ max taglen))
      (when (and (assoc tag simple-tigernote-tag-list)
                 (cdr (assoc tag simple-tigernote-tag-list)))
        (insert "\n"))
      (simple-tigernote-insert-tag-string tag t))))

(defun simple-tigernote-insert-tag (&optional tag)
  (interactive)
  "Insert a tag and put the cursor between the opening and closing tag."
  (unless tag
    (setq tag (simple-tigernote-get-tag)))
  (simple-tigernote-insert-tag-string tag)
  (save-excursion (simple-tigernote-insert-tag-string tag t))
  (when (and (assoc tag simple-tigernote-tag-list)
             (cdr (assoc tag simple-tigernote-tag-list)))
    (insert "\n")
    (save-excursion (insert "\n"))))

(if (featurep 'xemacs)
    (defun simple-tigernote-active-mark ()
      "Return non nil if the mark is active."
      (and zmacs-regions (mark)))
  (defun simple-tigernote-active-mark ()
    "Return non nil if the mark is active."
    (and transient-mark-mode mark-active)))

(defun simple-tigernote-insert-or-region-emph ()
  "Insert emphasized text.
If in `transient-mark-mode' and the region is active markup the region
emphasized."
  (interactive)
  (if (simple-tigernote-active-mark)
      (let ((beg (min (point) (mark))) (end (max (point) (mark))))
        (simple-tigernote-emph-region beg end))
    (simple-tigernote-insert-emph)))

(defun simple-tigernote-insert-or-region-strong ()
  "Insert strong text.
If in `transient-mark-mode' and the region is active markup the region
strong."
  (interactive)
  (if (simple-tigernote-active-mark)
      (let ((beg (min (point) (mark))) (end (max (point) (mark))))
        (simple-tigernote-strong-region beg end))
    (simple-tigernote-insert-strong)))

(defun simple-tigernote-insert-or-region-strong-emph ()
  "Insert strong emphasized text.
If in `transient-mark-mode' and the region is active markup the region
strong emphasized."
  (interactive)
  (if (simple-tigernote-active-mark)
      (let ((beg (min (point) (mark))) (end (max (point) (mark))))
        (simple-tigernote-strong-emph-region beg end))
    (simple-tigernote-insert-strong-emph)))

(defun simple-tigernote-insert-or-region-tag (&optional tag)
  "Insert opening and closing text around the cursor.
If in `transient-mark-mode' and the region is active put the tags around
the region."
  (interactive)
  (unless tag
    (setq tag (simple-tigernote-get-tag)))
  (if (simple-tigernote-active-mark)
      (let ((beg (min (point) (mark))) (end (max (point) (mark))))
        (simple-tigernote-tag-region beg end tag))
    (simple-tigernote-insert-tag tag)))



;; cursor movement

(defun simple-tigernote-next ()
  "Move the cursor to the beginning of the next link."
  (interactive)
  (let (pos1 pos2 (case-fold-search nil))
    (save-excursion
      (unless (equal simple-tigernote-link-pattern 'none)
        (when (re-search-forward (car simple-tigernote-link-pattern) nil t)
          (setq pos1 (match-beginning (cdr simple-tigernote-link-pattern))))))
    (save-excursion
      (unless (equal simple-tigernote-free-link-pattern 'none)
        (when (re-search-forward (car simple-tigernote-free-link-pattern) nil t)
          (setq pos2 (match-beginning (cdr simple-tigernote-free-link-pattern))))))
    (if (and pos1 pos2)
        (if (equal (min pos1 pos2) (point))
            (goto-char (max pos1 pos2))
          (goto-char (min pos1 pos2)))
      (if pos1
          (goto-char pos1)
        (if pos2
            (goto-char pos2))))))

(defun simple-tigernote-prev ()
  "Move the cursor to the beginning of the previous link"
  (interactive)
  (let (pos1 pos2 end-camelcase (case-fold-search nil))
    (save-excursion
      (unless (equal simple-tigernote-link-pattern 'none)
        (when (re-search-backward (car simple-tigernote-link-pattern) nil t)
          (setq pos1 (match-beginning (cdr simple-tigernote-link-pattern)))
          (setq end-camelcase (match-end (cdr simple-tigernote-link-pattern))))))
    (save-excursion
      (unless (equal simple-tigernote-free-link-pattern 'none)
        (when (re-search-backward (car simple-tigernote-free-link-pattern) nil t)
          (setq pos2 (match-beginning (cdr simple-tigernote-free-link-pattern))))))
    (if (and pos1 pos2)
        (if (and end-camelcase (equal (point) end-camelcase))
            (goto-char (min pos1 pos2))
          (goto-char (max pos1 pos2)))
      (if pos1
          (goto-char pos1)
        (if pos2
            (goto-char pos2))))))



;; mode definitions

(defun simple-tigernote-add-keyword (match-pair face overwrite)
  "Add an element to `simple-tigernote-font-lock-keywords'.
MATCH-PAIR has to be a pair with a regular expression and a
number for the subexpression: (REGEXP . NUMBER).  FACE is the
face used for highlighting and overwrite may be 'prepend,
'append, 'keep, t or nil.  See `font-lock-keywords'."
  (add-to-list
   'simple-tigernote-font-lock-keywords
   (cons (car match-pair) (list (cdr match-pair) `(quote ,face) overwrite))))

(defun simple-tigernote-add-font-lock-keywords ()
  "Add the default patterns to `simple-tigernote-font-lock-keywords'."

  ;; additional keywords
  (if (equal simple-tigernote-additional-keywords 'none)
      (setq simple-tigernote-font-lock-keywords nil)
    (setq simple-tigernote-font-lock-keywords simple-tigernote-additional-keywords))

  ;; local links
  (unless (equal simple-tigernote-link-pattern 'none)
    (simple-tigernote-add-keyword simple-tigernote-link-pattern
                             'simple-tigernote-local-link-face
                             'append))
  (unless (equal simple-tigernote-free-link-pattern 'none)
    (simple-tigernote-add-keyword simple-tigernote-free-link-pattern
                             'simple-tigernote-local-link-face
                             'append))
  ;; smilies
  (unless (equal simple-tigernote-smilies-pattern 'none)
    (simple-tigernote-add-keyword simple-tigernote-smilies-pattern
                             'simple-tigernote-smiley-face
                             t))
  ;; indent
  (unless (equal simple-tigernote-indent-pattern 'none)
    (simple-tigernote-add-keyword simple-tigernote-indent-pattern
                             'font-lock-comment-face
                             t))
  ;; horizontal lines
  (unless (equal simple-tigernote-horiz-line-pattern 'none)
    (simple-tigernote-add-keyword simple-tigernote-horiz-line-pattern
                             'font-lock-comment-face
                             t))
  ;; enums
  (unless (equal simple-tigernote-enum-pattern 'none)
    (simple-tigernote-add-keyword simple-tigernote-enum-pattern
                             'font-lock-constant-face
                             t))
  ;; bullet
  (unless (equal simple-tigernote-bullet-pattern 'none)
    (simple-tigernote-add-keyword simple-tigernote-bullet-pattern
                             'font-lock-keyword-face
                             t))
  ;;definition lists
  (unless (equal simple-tigernote-definition-pattern 'none)
    (simple-tigernote-add-keyword simple-tigernote-definition-pattern
                             'font-lock-type-face
                             t))
  ;; emphasis
  (let (em-re)
    (unless (equal simple-tigernote-em-patterns 'none)
      (when (setq em-re (first simple-tigernote-em-patterns))
        (simple-tigernote-add-keyword em-re 'simple-tigernote-emph-face 'append))
      (when (setq em-re (second simple-tigernote-em-patterns))
        (simple-tigernote-add-keyword em-re 'simple-tigernote-strong-face 'append))
      (when (setq em-re (third simple-tigernote-em-patterns))
        (simple-tigernote-add-keyword em-re
                                 'simple-tigernote-strong-emph-face
                                 'append))))
  ;; line breaks
  (unless (equal simple-tigernote-line-break-pattern 'none)
    (simple-tigernote-add-keyword simple-tigernote-line-break-pattern
                             'font-lock-warning-face
                             t))
  ;; head lines
  (let (head-re)
    (unless (equal simple-tigernote-headline-patterns 'none)
      (when (setq head-re (first simple-tigernote-headline-patterns))
        (simple-tigernote-add-keyword head-re 'simple-tigernote-heading-1-face t))
      (when (setq head-re (second simple-tigernote-headline-patterns))
        (simple-tigernote-add-keyword head-re 'simple-tigernote-heading-2-face t))
      (when (setq head-re (third simple-tigernote-headline-patterns))
        (simple-tigernote-add-keyword head-re 'simple-tigernote-heading-3-face t))
      (when (setq head-re (fourth simple-tigernote-headline-patterns))
        (simple-tigernote-add-keyword head-re 'simple-tigernote-heading-4-face t))
      ;; (when (setq head-re (fifth simple-tigernote-headline-patterns))
        ;; (simple-tigernote-add-keyword head-re 'simple-tigernote-heading-5-face t))
      ;; (when (setq head-re (sixth simple-tigernote-headline-patterns))
        ;; (simple-tigernote-add-keyword head-re 'simple-tigernote-heading-6-face t)) 
      )))

(defun simple-tigernote-define-major-mode (mode name doc-string &rest properties)
  "Define a major mode for editing a tigernote page.
MODE has to be a symbol which is used to build the major mode command:
e.g. 'emacstigernote results in the command `simple-emacstigernote-mode'. NAME
is a string which will appear in the status line (e.g. \"EmacsTigernote\").
DOC-STRING is an an optional documentation string.  See
`definde-derived-mode'

To overwrite the default syntax (that should be fine for emacstigernote or
any default oddmuse installation) you can specify various properties
as a list of keywords:

        :tags............... overwrite `simple-tigernote-tag-list'
        :camelcase.......... overwrite `simple-tigernote-link-pattern'
        :free-link.......... overwrite `simple-tigernote-free-link-pattern'
        :smilies............ overwrite `simple-tigernote-smilies-pattern'
        :em-strings......... overwrite `simple-tigernote-em-strings'
        :strong-strings..... overwrite `simple-tigernote-strong-strings'
        :strong-em-strings.. overwrite `simple-tigernote-strong-em-strings'
        :em-patterns........ overwrite `simple-tigernote-em-patterns'
        :headlines.......... overwrite `simple-tigernote-headline-patterns'
        :keywords........... overwrite `simple-tigernote-additional-keywords'
        :outline............ overwrite `simple-tigernote-outline-patterns'
        :linebreak.......... overwrite `simple-tigernote-line-break-pattern'
        :horiz.............. overwrite `simple-tigernote-horiz-line-pattern'
        :enum............... overwrite `simple-tigernote-enum-pattern'
        :bullet............. overwrite `simple-tigernote-bullet-pattern'
        :indent............. overwrite `simple-tigernote-indent-pattern'
        :deflist............ overwrite `simple-tigernote-definition-pattern'

Use the symbol 'none as the value if the tigernote doesn't support the property."
  (eval
   `(define-derived-mode
      ,(intern (concat "simple-" (symbol-name mode) "-mode"))
      text-mode ,name ,doc-string

      ;; ugly!  ugly!  ugly!
      (dolist (pair
               (list
                (cons 'simple-tigernote-tag-list
                      (quote ,(plist-get properties :tags)))
                (cons 'simple-tigernote-link-pattern
                      (quote ,(plist-get properties :camelcase)))
                (cons 'simple-tigernote-free-link-pattern
                      (quote ,(plist-get properties :free-link)))
                (cons 'simple-tigernote-smilies-pattern
                      (quote ,(plist-get properties :smilies)))
                (cons 'simple-tigernote-em-strings
                      (quote ,(plist-get properties :em-strings)))
                (cons 'simple-tigernote-strong-strings
                      (quote ,(plist-get properties :strong-strings)))
                (cons 'simple-tigernote-strong-em-strings
                      (quote ,(plist-get properties :strong-em-strings)))
                (cons 'simple-tigernote-em-patterns
                      (quote ,(plist-get properties :em-patterns)))
                (cons 'simple-tigernote-headline-patterns
                      (quote ,(plist-get properties :headlines)))
                (cons 'simple-tigernote-additional-keywords
                      (quote ,(plist-get properties :keywords)))
                (cons 'simple-tigernote-outline-patterns
                      (quote ,(plist-get properties :outline)))
                (cons 'simple-tigernote-line-break-pattern
                      (quote ,(plist-get properties :linebreak)))
                (cons 'simple-tigernote-horiz-line-pattern
                      (quote ,(plist-get properties :horiz)))
                (cons 'simple-tigernote-enum-pattern
                      (quote ,(plist-get properties :enum)))
                (cons 'simple-tigernote-bullet-pattern
                      (quote ,(plist-get properties :bullet)))
                (cons 'simple-tigernote-indent-pattern
                      (quote ,(plist-get properties :indent)))
                (cons 'simple-tigernote-definition-pattern
                      (quote ,(plist-get properties :deflist)))
                (cons 'simple-tigernote-outline-patterns
                      (quote ,(plist-get properties :outline)))))
        (when (cdr pair)
          (set (make-local-variable (car pair)) (cdr pair))))

      (unless (equal simple-tigernote-outline-patterns 'none)
        (setq outline-regexp (car simple-tigernote-outline-patterns))
        (setq outline-heading-end-regexp (cdr simple-tigernote-outline-patterns)))

      (define-key ,(intern (concat "simple-" (symbol-name mode) "-mode-map"))
        "\C-c\C-e" 'simple-tigernote-insert-or-region-emph)
      (define-key ,(intern (concat "simple-" (symbol-name mode) "-mode-map"))
        "\C-c\C-s" 'simple-tigernote-insert-or-region-strong)
      (define-key ,(intern (concat "simple-" (symbol-name mode) "-mode-map"))
        "\C-c\C-t" 'simple-tigernote-insert-or-region-tag)
      (define-key ,(intern (concat "simple-" (symbol-name mode) "-mode-map"))
        "\C-c\C-n" 'simple-tigernote-next)
      (define-key ,(intern (concat "simple-" (symbol-name mode) "-mode-map"))
        "\C-c\C-p" 'simple-tigernote-prev)

      (make-local-variable 'font-lock-defaults)
      (setq font-lock-multiline t)
      (simple-tigernote-add-font-lock-keywords)
      (setq font-lock-defaults  '(simple-tigernote-font-lock-keywords t))
      (goto-address)
      (font-lock-mode 1)
      (setq indent-tabs-mode nil)
      (run-hooks 'simple-tigernote-common-hook))))



;; mode definitions

;; oddmuse tigernotes

;; for historical reasons define `simple-tigernote-mode'
(simple-tigernote-define-major-mode
 'tigernote
 "Tigernote"
 "Simple mode to edit tigernote pages.
\\{simple-tigernote-mode-map}")

(simple-tigernote-define-major-mode
 'emacstigernote
 "EmacsTigernote"
  "Simple mode to edit tigernote pages at http://www.emacstigernote.org/.
\\{simple-emacstigernote-mode-map}")

(simple-tigernote-define-major-mode
 'oddmuse
 "OddMuse"
 "Simple mode to edit tigernote pages at http://www.oddmuse.org/.
\\{simple-oddmuse-mode-map}"
 :camelcase 'none)



;; mediatigernote

(simple-tigernote-define-major-mode
 'mediatigernote
 "MediaTigernote"
 "Simple mode to edit mediatigernote pages.
\\{simple-mediatigernote-mode-map}"
 :camelcase 'none

 :smilies 'none

 :linebreak '("<br>" . 0)

 :tags '(("b" . nil) ("big" . nil) ("blockquote" . nil) ("caption" . nil)
         ("code" . nil) ("center" . nil) ("cite" . nil) ("dfn" . nil)
         ("dl" . nil) ("em" . nil) ("i" . nil) ("kbd" . nil) ("math" . nil)
         ("notigernote" . nil) ("ol" . nil) ("pre" . nil) ("samp" . nil)
         ("small" . nil) ("strike" . nil) ("strong" . nil) ("sub" . nil)
         ("sup" . nil) ("tt" . nil) ("u" . nil) ("ul" . nil) ("var" . nil)
         ("a" . nil) ("div" . nil) ("font" . nil) ("table" . nil) ("td" . nil)
         ("tr" . nil))

 :keywords
 (list
  '(simple-tigernote-match-tag-i . (0 'simple-tigernote-italic-face append))
  '(simple-tigernote-match-tag-b . (0 'simple-tigernote-bold-face append))
  '(simple-tigernote-match-tag-u . (0 'simple-tigernote-underline-face append))
  '(simple-tigernote-match-tag-tt . (0 'simple-tigernote-teletype-face append))
  '(simple-tigernote-match-tag-em . (0 'simple-tigernote-emph-face append))
  '(simple-tigernote-match-tag-strong . (0 'simple-tigernote-strong-face append))
  '(simple-tigernote-match-tag-math . (0 'font-lock-string-face append))
  '(simple-tigernote-match-tag-strike . (0 'simple-tigernote-strike-face append))
  '(simple-tigernote-match-tag-code . (0 'simple-tigernote-code-face append))

  ;; tags
  (list (concat "\\(</?\\)"
                "\\([A-Za-z]+\\)"
                "\\(\\([ \t]+[a-zA-Z]+\\)=\\(\".*\"\\)\\)*"
                "\\(/?>\\)?")
        '(1 'default t t)
        '(2 'font-lock-function-name-face t t)
        '(4 'font-lock-variable-name-face t t)
        '(5 'font-lock-string-face t t)
        '(6 'default t t))

  ;; again.  otherwise overwritten by tag highlight.
  '("<br>" . (0 'font-lock-warning-face t))

  '(simple-tigernote-match-tag-notigernote . (0 'simple-tigernote-notigernote-face t))
  '(simple-tigernote-match-tag-pre . (0 'simple-tigernote-code-face t))

  '("^ .*$" . (0 'simple-tigernote-code-face t))))



;; phptigernote

(simple-tigernote-define-major-mode
 'phptigernote
 "PhpTigernote"
 "Simple mode to edit php tigernote pages.
\\{simple-phptigernote-mode-map}"

 :camelcase
 (if (featurep 'xemacs)
     ;; FIXME: no character classes.  only ascii chars will work.
     (cons (concat "\\([^~]\\|^\\)"
                   "\\<\\([A-Z][a-z]+"
                   "\\([A-Z][a-z]+\\)+\\)\\(\\>\\|'\\)")  2)
   (cons (concat "\\([^~]\\|^\\)"
                 "\\<\\([[:upper:]][[:lower:]]+"
                 "\\([[:upper:]][[:lower:]]+\\)+\\)\\(\\>\\|'\\)")  2))

 :free-link '("\\(^\\|[^~]\\)\\[\\([^\n]+?\\)\\]" . 2)

 :tags '(("pre" . t) ("verbatim" . t) ("b" . nil) ("big" . nil) ("i" . nil)
         ("small" . nil) ("tt" . nil) ("em" . nil) ("strong" . nil)
         ("abbr" . nil) ("acronym" . nil) ("cite" . nil) ("code" . nil)
         ("dfn" . nil) ("kbd" . nil) ("samp" . nil) ("var" . nil)
         ("sup" . nil) ("sub" . nil))

 :headlines '(("^[ \t]*!!!\\(.*?\\)$" . 1)
              ("^[ \t]*!!\\([^!].*?\\)$" . 1)
              ("^[ \t]*!\\([^!].*?\\)$" . 1)
              nil nil nil)

 :outline '("[ \t]*!+" . "\n")

 :em-strings '("_" . "_")

 :strong-strings '("*" . "*")

 :strong-em-strings '("_*" . "*_")

 ;; FIXME: this works not well with font-lock...
 :deflist '("^\\([^\n]+:\\)[ \t]*\n[ \t]+.*?" . 1)

 :em-patterns (list '("\\(\\W\\|^\\)_.*?_" . 0)
                    '("\\W\\*.*?\\*" . 0) ; bold at bol is a bullet list
                    (cons (concat "\\(\\(\\W\\|^\\)_\\*\\|\\W\\*_\\)"
                                  ".*?\\(\\_*\\|\\*_\\)")  0))

 :enum '("^\\([-*#o+ \t]*#+\\)\\([^-#*+]\\|$\\)" . 1)

 :bullet '("^\\([-*#o+ \t]*\\([-*+]\\|o[ \t]+\\)\\)\\([^-*#+]\\|$\\)" . 1)

 :smilies 'none

 :linebreak '("%%%" . 0)

 :indent 'none

 :keywords
 (list
  '(simple-tigernote-match-tag-i . (0 'simple-tigernote-italic-face append))
  '(simple-tigernote-match-tag-b . (0 'simple-tigernote-bold-face append))
  '(simple-tigernote-match-tag-tt . (0 'simple-tigernote-teletype-face append))
  '(simple-tigernote-match-tag-em . (0 'simple-tigernote-emph-face append))
  '(simple-tigernote-match-tag-strong . (0 'simple-tigernote-strong-face append))
  '(simple-tigernote-match-tag-code . (0 'simple-tigernote-code-face append))
  '(simple-tigernote-match-tag-pre . (0 'simple-tigernote-code-face append))

  '("\\(\\W\\|^\\)=.*?=" . (0 'simple-tigernote-teletype-face append))

  ;; tags FIXME: highlight plugins instead of parameters
  (list (concat "\\(</?\\)"
                "\\([A-Za-z]+\\)"
                "\\(\\([ \t]+[a-zA-Z]+\\)=\\(\".*\"\\)\\)*"
                "\\(/?>\\)?")
        '(1 'default t t)
        '(2 'font-lock-function-name-face t t)
        '(4 'font-lock-variable-name-face t t)
        '(5 'font-lock-string-face t t)
        '(6 'default t t))

  '(simple-tigernote-match-tag-verbatim . (0 'simple-tigernote-code-face t))))




;; jsptigernote

(simple-tigernote-define-major-mode
 'jsptigernote
 "JspTigernote"
 "Simple mode to edit jsp tigernote pages.
\\{simple-jsptigernote-mode-map}"

 ;; not the default but enabled on http://jsptigernote.org
 :camelcase
 (if (featurep 'xemacs)
     ;; FIXME: no character classes.  only ascii chars will work.
     (cons (concat "\\([^~]\\|^\\)"
                   "\\(\\<[A-Z]+[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\\>\\)") 2)
   (cons (concat "\\([^~]\\|^\\)"
                 "\\<\\([[:upper:]]+[[:lower:]][[:alnum:]]*"
                 "[[:upper:]][[:alnum:]]*\\>\\)") 2))

 :free-link '("\\(^\\|[^[]\\)\\[\\([^[][^\n]+?\\)\\]" . 2)

 ;; really?
 :tags 'none

 :headlines '(("^[ \t]*!!!\\(.*?\\)$" . 1)
              ("^[ \t]*!!\\([^!].*?\\)$" . 1)
              ("^[ \t]*!\\([^!].*?\\)$" . 1)
              nil nil nil)

 :outline '("[ \t]*!+" . "\n")

 :strong-strings '("__" . "__")

 :indent '("^;[ \t]*:" . 0)

 :deflist '("^\\(;+[ \t]*[^ \t]+?:\\)" . 1)

 :em-patterns (list '("\\(\\W\\|^\\)''.*?''" . 0)
                    '("\\(\\W\\|^\\)__.*?__" . 0)
                    (cons (concat "\\(\\W\\|^\\)\\(''__\\|__''\\)"
                                  ".*?\\(__''\\|''__\\)")  0))

 :linebreak '("\\\\\\\\" . 0)

 :keywords
 (list
  '("\\(\\W\\|^\\)\\({{[^{].*?}}\\)" .
    (2 'simple-tigernote-teletype-face append))
  '(simple-tigernote-match-code-jsp . (0 'simple-tigernote-code-face t))))



(provide 'simple-tigernote)

;;; simple-tigernote.el ends here
